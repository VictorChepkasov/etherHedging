// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/security/PullPayment.sol";

contract Hedging is PullPayment {
    uint bank = 0;
    //если контракт активирован, то нужно дождаться n дней до реактивации,
    // и в это время нельзя положить\забрать оттуда эфиры
    struct Hedge {
        bool contractActivate;
        bool contractReactivate; //если реактивирован, то сторонам начисляется эфир
        address payable partyA;
        address payable partyB;
        uint ethUSDData; //цена пары eth/usd, будет браться из оракула
        uint shelfLife; //n дней, после которых активируется контракт
        uint dateOfCreate; //от этой даты отсчитываем n дней
        uint dateOfReactivate; //дата, после которой можно реактивировать контракт
        uint dateOfClose; //дата закрытия сделки
    }
    mapping(address => bool) inputsEth; //ввели ли строны эфир
    mapping(address => bool) receivedEth; //получили ли деньги стороны после реактивации контракта 
    mapping(address => uint) balances; //балансы сторон в долларах

    Hedge private hedge;
    AggregatorV3Interface public dataFeed;

    /*
    * Aggregator: ETH/USD
    * Network: Sepolia
    * Address: 0x694AA1769357215DE4FAC081bf1f309aDC325306
    */

    modifier onlyParties() {
        require(
            msg.sender == hedge.partyA || msg.sender == hedge.partyB,
            "Only parties!"
        );
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

    receive() external payable {
        bank += msg.value;
    }

    fallback() external payable {}

    constructor(address dataFeedAddress) {
        dataFeed = AggregatorV3Interface(dataFeedAddress);
        hedge.partyA = payable(msg.sender);
    }

    function getContractBalance() external view returns(uint) {
        return address(this).balance;
    }

    function getHedgeInfo() external view returns(
        Hedge memory, bool, bool, bool, bool, uint, uint
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

    function setHedgeInfo(
        address _partyB,
        uint _shelfLife
    ) 
        public contractNonActive 
    {
        require(
            hedge.partyA != _partyB,
            "Party A and party B must be different persons!"
        );
        hedge.partyB = payable(_partyB);
        hedge.ethUSDData = getLatestETHUSDData(); 
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
        hedge.ethUSDData = getLatestETHUSDData();

        //проверяем одиноковую ли сумму ввели стороны
        if (balances[hedge.partyA] != 0 && balances[hedge.partyB] != 0) {
            require(
                balances[msg.sender] == msg.value * hedge.ethUSDData,
                "The parties entered different amounts of funds!"
            );
        }

        _asyncTransfer(payable(address(this)), msg.value);
        require(payments(address(this)) > 0, "No payments to withdraw!");
        withdrawPayments(payable(address(this)));

        inputsEth[msg.sender] = true;
        balances[msg.sender] = msg.value * hedge.ethUSDData;

        if (inputsEth[hedge.partyA] && inputsEth[hedge.partyB]) {
            _setContractActivate();
        }
    }

    function setContractReactivate() public contractActive onlyParties {
        require(
            block.timestamp >= hedge.dateOfReactivate,
            "The time hasn't yet come!"
        );
        hedge.ethUSDData = getLatestETHUSDData();
        
        uint newABalance = (address(this).balance / 2) / hedge.ethUSDData; 
        uint newBBalance = address(this).balance - newABalance;
        receivedEth[hedge.partyA] = true;
        receivedEth[hedge.partyB] = true;
        hedge.dateOfClose = block.timestamp;

        _asyncTransfer(hedge.partyA, newABalance); //A 
        _asyncTransfer(hedge.partyB, newBBalance); //B
    }

    function getLatestETHUSDData() public view returns (uint) {
        (
            /* uint80 roundID */,
            int answer,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = dataFeed.latestRoundData();
        return uint(answer);
    }

    function _setContractActivate() private contractNonActive {
        hedge.dateOfCreate = block.timestamp;
        hedge.dateOfReactivate = hedge.dateOfCreate + hedge.shelfLife;
        hedge.contractActivate = true;
    }

    function _withdraw() private {
        require(msg.sender != address(0), "Wrong address!");
        uint amount = payments(msg.sender);
        require(amount > 0, "No payments to withdraw!");
        withdrawPayments(payable(msg.sender));
    }
}