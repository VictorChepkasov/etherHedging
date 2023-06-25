// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Hedging {
    uint bank = 0;
    //если контракт активирован, то нужно дождаться n дней до реактивации,
    // и в это время нельзя положить\забрать оттуда эфиры
    struct Hedge {
        bool contractActivate;
        bool contractReactivate; //если реактивирован, то сторонам начисляется эфир
        address payable partyA;
        address payable partyB;
        uint ethUSDPrice; //цена пары eth/usd, будет браться из оракула
        uint shelfLife; //n дней, после которых активируется контракт
        uint dateOfCreate; //от этой даты отсчитываем n дней
        uint dateOfReactivate; //дата, после которой можно реактивировать контракт
        uint dateOfClose; //дата закрытия сделки
    }
    mapping(address => bool) inputsEth; //ввели ли строны эфир
    mapping(address => bool) receivedEth; //получили ли деньги стороны после реактивации контракта 
    mapping(address => uint) balances; //балансы сторон в долларах

    Hedge private hedge;

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
        //потом подключим оракул, 2 знака после запятой (1903,65)
        hedge.ethUSDPrice = 190365; 
        hedge.shelfLife = 86400 * _shelfLife;
        hedge.dateOfReactivate = 0;
        inputsEth[hedge.partyA] = false;
        inputsEth[hedge.partyB] = false;
        receivedEth[hedge.partyA] = false;
        receivedEth[hedge.partyB] = false;
        balances[hedge.partyA] = 0;
        balances[hedge.partyB] = 0;
    }

    function pay() public payable onlyParties contractNonActive {
        require(
            !hedge.contractReactivate,
            "Contract reactive!"
        );

        //проверяем одиноковую ли сумму ввели стороны
        if (balances[hedge.partyA] != 0 && balances[hedge.partyB] != 0) {
            require(
                balances[msg.sender] == msg.value * hedge.ethUSDPrice,
                "The parties entered different amounts of funds!"
            );
        }

        balances[msg.sender] = msg.value * hedge.ethUSDPrice;
        inputsEth[msg.sender] = true;
        _withdraw(payable(address(this)), msg.value);

        if (inputsEth[hedge.partyA] && inputsEth[hedge.partyB]) {
            setContractActivate();
        }
    }

    function setContractActivate() public contractNonActive {
        hedge.dateOfCreate = block.timestamp;
        hedge.dateOfReactivate = hedge.dateOfCreate + hedge.shelfLife;
        hedge.contractActivate = true;
    }

    function setContractReactivate() public contractActive onlyParties {
        require(
            block.timestamp >= hedge.dateOfReactivate,
            "The time hasn't yet come!"
        );
        hedge.contractReactivate = true;

        //возможно, примерно так, но это без оракула
        uint newABalance = (address(this).balance / 2) / hedge.ethUSDPrice; 
        uint newBBalance = address(this).balance - hedge.newABalance;
        receivedEth[hedge.partyA] = true;
        _withdraw(hedge.partyA, newABalance); //A 
        receivedEth[hedge.partyB] = true;
        _withdraw(hedge.partyB, newBBalance); //B

        hedge.dateOfClose = block.timestamp;
    }

    function getContractBalance() public view returns(uint) {
        return address(this).balance;
    }

    function getHedgeInfo() public view returns(
        Hedge memory, uint, uint, uint, uint, uint, uint
    ) {
        return (
            hedge,
            inputsEth[hedge.partyA],
            inputsEth[hedge.partyB],
            receivedEth[hedge.partyA],
            receivedEth[hedge.partyB],
            balances[hedge.partyA],
            balances[hedge.partyB]
        );
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
    modifier onlyParties() {
        require(msg.sender == hedge.partyA || msg.sender == hedge.partyB, "Only parties!");
        _;
    }

    modifier onlyA() {
        require(msg.sender == hedge.partyA, "Only party A!");
        _;
    }
    modifier onlyB() {
        require(msg.sender == hedge.partyB, "Only party B!");
        _;
    }

    modifier contractActive() {
        require(hedge.contractActivate, "Contract must activate!");
        _;
    }
    modifier contractNonActive() {
        require(
            !hedge.contractActivate && !hedge.contractReactivate,
            "Contract active!"
        );
        _;
    }
}