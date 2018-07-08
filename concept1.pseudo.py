def tx_execute_before(from, to, value, gasLimit, gasPrice, data) :
    # 1. check intrinsic gas + value
    balance = getBalance(from)
    assert balance >= value + gasLimit * gasPrice

    # 2. substract gas + value
    substractBalance(from, balance - value - gasLimit * gasPrice)

    # 3. execute EVM
    executeVM(from, to, value, gasLimit, gasPrice, data)

    # 4. collect refunded gas
    addBalance(from, gasRemained * gasPrice)

def tx_execute_after(from, to, value, gasLimit, gasPrice, data) :
    # 0. get delegatee, execute EVM
    delegatee = staminaContract.delegatee(to)

    # 1. case where delegatee exist
    if delegatee:
        # 1-1. check intrinsic gas if `to` is delegatee/stamina contract
        assert staminaContract.balanceOf(delegatee) >= gasLimit * gasPrice

        # 1-2. substract gas from delegatee
        staminaContract.substractBalance(delegatee, gasLimit * gasPrice)

        # 1-3. subtract value from "from" account
        subtractBalance(from, value)

        # 1-4. execute EVM
        executeVM(from, to, value, gasLimit, gasPrice, data)

        # 1-5. collect refunded gas
        staminaContract.addBalance(delegatee, gasRemained * gasPrice)

    # 2. case where delegatee does not exist
    else:
        # 2-1. Execute Tx Traditional way
        tx_execute_before(from, to, value, gasLimit, gasPrice, data)
