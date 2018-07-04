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

# "delegatee" is optional field in transaction
def tx_execute_after(from, to, value, gas, gasPrice, data, delegatee=none):
    # 1. check if delegatee passed or not
    if delegatee:
        # 1-1. check if (`to`, `delegatee`) tuple is registered in staminaContract
        if staminaContract.registered(to, delegatee):
            # 1-1-1. check if `delegatee` can pay upfront cost(only gas * gasPrice)
            assert staminaContract.balanceOf(delegatee) >= gas * gasPrice
            
            # 1-1-2. check if `from` can pay upfront cost(only value)
            assert getBalance(from) >= value

            # 1-1-3. subtract upfront cost(only gas * gasPrice) from `delegatee`
            staminaContract.subtractBalance(delegatee, gas * gasPrice)
            
            # 1-1-4. subtract upfront cost(only value) from `from`
            subtractBalance(from, value)

            # 1-1-5. execute EVM
            executeVM(from, to, value, gas, gasPrice, data)

            # 1-1-6. collect refunded gas
            staminaContract.addBalance(delegatee, remainedGas * gasPrice)

        # 1-2 case where delegatee is not registered
        else:
            # "delegatee" account is in transaction but does not registered to staminaContract
            raise # throw if (`to`, `delegatee`) tuple is not registered

    # 2. transaction without delegatee. same logic as original version
    else:
        return tx_execute_before(from, to, value, gas, gasPrice, data)
