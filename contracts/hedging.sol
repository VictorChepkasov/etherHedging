// SPDX-License-Identifier: MIT
pragma solidity >=0.8.10 <0.9.0;

contract Hedging {
    address payable bank = payable(address(this));
    //если контракт активирован, то нужно дождаться n дней до реактивации,
    // и в это время нельзя положить\забрать оттуда эфиры
    bool contractActivate = false;
    bool contractReactivate = false; //если реактивирован, то сторонам начисляется эфир

    struct HedgeInfo {
        address payable partyA;
        address payable partyB;

        //балансы сторон в долларах
        uint aBalance;
        uint bBalance;
        uint ethUSDPrice; //цена пары eth/usd, будет браться из оракула
        uint shelfLife; //n дней, после которых активируется контракт
        uint dateOfCreate; //от этой даты отсчитываем n дней
        uint dateOfReactivate; //дата, после которой можно реактивировать контракт
        uint dateOfClose; //дата закрытия сделки
        
        //ввели ли строны эфир
        bool partyAInputEth;
        bool partyBInputEth;
        //получили ли деньги стороны после реактивации контракта 
        bool partyAReceivedEth;
        bool partyBReceivedEth;
    }

    HedgeInfo private hedge;

    constructor() {
        hedge.partyA = payable(msg.sender);
    }

    receive() external payable {}

    function setHedgeInfo(
        address _partyB,
        uint _shelfLife
    ) public contractNonActive {
        require(msg.sender != _partyB, "Party A and party B must be different persons!");
        hedge.partyB = payable(_partyB);
        hedge.aBalance = 0;
        hedge.bBalance = 0;
        hedge.ethUSDPrice = 190365; //потом подключим оракул, 2 знака после запятой (1903,65)
        hedge.shelfLife = _shelfLife * 86400;
        hedge.dateOfReactivate = 0;
        hedge.partyAInputEth = false;
        hedge.partyBInputEth = false;
        hedge.partyAReceivedEth = false;
        hedge.partyBReceivedEth = false;
    }

    function payPartyA(uint _value) payable public onlyA contractNonActive {
        require(!contractActivate || !contractReactivate, "Contract active or reactive!");
        //проверяем одиноковую ли сумму ввели стороны
        if (hedge.bBalance != 0) {
            require(hedge.bBalance == _value * hedge.ethUSDPrice, "The parties entered different amounts of funds!");
            hedge.aBalance = _value * hedge.ethUSDPrice;
        } else {
            hedge.aBalance = _value * hedge.ethUSDPrice;
        }

        _payParty(msg.sender, _value);

        if (hedge.partyBInputEth) {
            setContractActivate();
        }
    }

    function payPartyB(uint _value) payable public onlyB contractNonActive {
        

        if (hedge.aBalance != 0) {
            require(hedge.aBalance == _value * hedge.ethUSDPrice, "The parties entered different amounts of funds!");
            hedge.bBalance = _value * hedge.ethUSDPrice;
        } else {
            hedge.bBalance = _value * hedge.ethUSDPrice;
        }

        _payParty(msg.sender, _value);

        if (hedge.partyAInputEth) {
            setContractActivate();
        }
    }

    function setContractActivate() public contractNonActive {
        hedge.dateOfCreate = block.timestamp;
        hedge.dateOfReactivate = hedge.dateOfCreate + hedge.shelfLife;
        contractActivate = true;
    }

    function setContractReactivate() public contractActive onlyParty {
        require(block.timestamp >= hedge.dateOfReactivate, "The time hasn't yet come!");
        contractReactivate = true;

        //возможно, примерно так, но это без оракула
        uint newABalance = (bank.balance / 2) / hedge.ethUSDPrice; 
        uint newBBalance = bank.balance - newABalance;
        _payParty(hedge.partyA, newABalance); //A 
        hedge.partyAReceivedEth = true;
        _payParty(hedge.partyB, newBBalance); //B
        hedge.partyBReceivedEth = true;

        hedge.dateOfClose = block.timestamp;
    }

    function getContractBalance() public view returns(uint) {
        return bank.balance;
    }

    function getHedgeInfo() public view returns(HedgeInfo memory) {
        return hedge;
    }

    function _payParty(address _sender, uint _value) private {
        require(_sender != address(0), "Wrong address!");
        hedge.partyBInputEth = true;
        bool sent = bank.send(_value);
        require(sent, "Failure! Ether not sent!");
    }

    //модификаторы
    modifier onlyA() {
        require(msg.sender == hedge.partyA, "Only party A!");
        _;
    }
    modifier onlyB() {
        require(msg.sender == hedge.partyB, "Only party B!");
        _;
    }
    modifier onlyParty() {
        require(msg.sender == hedge.partyA || msg.sender == hedge.partyB, "Only party!");
        _;
    }
    modifier contractActive() {
        require(contractActivate, "Contract must activate!");
        _;
    }
    modifier contractNonActive() {
        require(!contractActivate && !contractReactivate, "Contract active!");
        _;
    }
}