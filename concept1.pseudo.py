def tx_execute_before(from, to, value, gas, gasPrice, data) :
    # 1. check `from` can pay upfront cost
    balance = getBalance(from)
    assert balance >= value + gas * gasPrice

    # 2. subtract upfront cost(tx.value + tx.gas * tx.gasPrice)
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
        # 1-1. if `to` has delegatee check upfront cost(only gas*gasPrice) 
        assert staminaContract.balanceOf(delegatee) >= gas * gasPrice

        # 1-2. subtract upfront cost(only gas*gasPrice) from delegatee
        staminaContract.subtractBalance(delegatee, gas * gasPrice)

        # 1-3. subtract upfront cost(only value)
        subtractBalance(from, value)
    # 2. case where delegatee does not exist
    else:
        # 2-1. check `from` can pay upfront cost
        balance = getBalance(to)
        assert balance >= value + gas * gasPrice

        # 2. subtract gas + value
        subtractBalance(to, balance - value + gas * gasPrice)

    # 3. execute EVM
    executeVM(from, to, value, gas, gasPrice, data)

    # 4. collect refunded gas
    addBalance(from, remainedGas * gasPrice)
