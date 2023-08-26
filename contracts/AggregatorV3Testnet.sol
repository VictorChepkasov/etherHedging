// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// Этот контракт - заглушка для тестирования в сети разработки (development), т.к. это будет наммного быстрее
// метод для получения настоящих котировок будет протестирован отдельно
contract AggregatorV3Testnet {
    function latestRoundData() 
        external
        view
        returns(
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
    ) {
        return (2, 165119110000, block.timestamp, block.timestamp + 30, 1651);
    }
}