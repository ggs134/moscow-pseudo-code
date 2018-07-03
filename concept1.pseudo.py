def tx_execute_before(from, to, value, gas, gasPrice, data) :
    # 1. check intrinsic gas + value
    balance = getBalance(from)
    assert balance >= value + gas * gasPrice

    # 2. subtract gas + value
    subtractBalance(from, balance - value + gas * gasPrice)

    # 3. execute EVM
    executeVM(from, to, value, gas, gasPrice, data)

    # 4. collect refunded gas
    addBalance(from, remainedGas * gasPrice)

def tx_execute_after(from, to, value, gas, gasPrice, data) :
    # 0. get delegatee, execute EVM
    delegatee = staminaContract.delegatee(to)

    # 1. case where delegatee exist
    if delegatee:
        # 1-1. check intrinsic gas if `to` has delegatee
        assert staminaContract.balanceOf(delegatee) >= gas * gasPrice

        # 1-2. subtract gas from delegatee
        staminaContract.subtractBalance(delegatee, gas * gasPrice)

        # 1-3. subtract value
        subtractBalance(from, value)
    # 2. case where delegatee does not exist
    else:
        # 2-1. check intrinsic gas + value
        balance = getBalance(to)
        assert balance >= value + gas * gasPrice

        # 2. subtract gas + value
        subtractBalance(to, balance - value + gas * gasPrice)

    # 3. execute EVM
    executeVM(from, to, value, gas, gasPrice, data)

    # 4. collect refunded gas
    addBalance(from, remainedGas * gasPrice)
