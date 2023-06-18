// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Hedging {
    uint256 bank = 0;
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

    function setHedgeInfo(
        address _partyB,
        uint _shelfLife
    ) public contractNonActive {
        require(
            hedge.partyA != _partyB,
            "Party A and party B must be different persons!"
        );
        hedge.partyB = payable(_partyB);
        hedge.aBalance = 0;
        hedge.bBalance = 0;
        //потом подключим оракул, 2 знака после запятой (1903,65)
        hedge.ethUSDPrice = 190365; 
        hedge.shelfLife = 86400 * _shelfLife;
        hedge.dateOfReactivate = 0;
        hedge.partyAInputEth = false;
        hedge.partyBInputEth = false;
        hedge.partyAReceivedEth = false;
        hedge.partyBReceivedEth = false;
    }

    function payPartyA() payable public onlyA contractNonActive {
        require(
            !contractActivate || !contractReactivate,
            "Contract active or reactive!"
        );
        //проверяем одиноковую ли сумму ввели стороны
        if (hedge.bBalance != 0) {
            require(
                hedge.bBalance == msg.value * hedge.ethUSDPrice,
                "The parties entered different amounts of funds!"
            );
        }

        hedge.aBalance = msg.value * hedge.ethUSDPrice;
        hedge.partyAInputEth = true;
        _withdraw(payable(address(this)), msg.value);

        if (hedge.partyBInputEth) {
            setContractActivate();
        }
    }

    function payPartyB() payable public onlyB contractNonActive {
        require(
            !contractActivate || !contractReactivate,
            "Contract active or reactive!"
        );
        //проверяем одиноковую ли сумму ввели стороны
        if (hedge.aBalance != 0) {
            require(
            hedge.aBalance == msg.value * hedge.ethUSDPrice,
            "The parties entered different amounts of funds!"
        );
        }

        hedge.bBalance = msg.value * hedge.ethUSDPrice;
        hedge.partyBInputEth = true;
        _withdraw(payable(address(this)), msg.value);

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
        require(
            block.timestamp >= hedge.dateOfReactivate,
            "The time hasn't yet come!"
        );
        contractReactivate = true;

        //возможно, примерно так, но это без оракула
        uint newABalance = (address(this).balance / 2) / hedge.ethUSDPrice; 
        uint newBBalance = address(this).balance - newABalance;
        hedge.partyAReceivedEth = true;
        _withdraw(hedge.partyA, newABalance); //A 
        hedge.partyBReceivedEth = true;
        _withdraw(hedge.partyB, newBBalance); //B

        hedge.dateOfClose = block.timestamp;
    }

    function getContractBalance() public view returns(uint) {
        return address(this).balance;
    }

    function getHedgeInfo() public view returns(HedgeInfo memory) {
        return hedge;
    }

    function _withdraw(address _to, uint256 _value) private {
        require(msg.sender != address(0), "Wrong address!");
        (bool sent, ) = _to.call{value: _value}("");
        require(sent, "Failed to send Ether");
    }

    receive() external payable {
        bank += msg.value;
    }

    fallback() external payable {}

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
        require(
            msg.sender == hedge.partyA || msg.sender == hedge.partyB,
            "Only party!"
        );
        _;
    }
    modifier contractActive() {
        require(contractActivate, "Contract must activate!");
        _;
    }
    modifier contractNonActive() {
        require(
            !contractActivate && !contractReactivate,
            "Contract active!"
        );
        _;
    }
}