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

# "delegatee" is optional in transaction
def tx_execute_after(from, to, value, gas, gasPrice, data, delegatee=none):
    # 1. check if delegatee passed or not
    if delegatee:
        # 1-1. check if delegatee account registered in staminaContract, executeVM
        if (staminaContract.isDelegatee(delegatee)):

            # 1-1-1. check intrinsic gas if `delegatee` has delegatee
            assert staminaContract.balanceOf(delegatee) >= gas * gasPrice

            # 1-1-2. subtract gas from delegatee
            staminaContract.subtractBalance(delegatee, gas * gasPrice)

            # 1-1-3. execute EVM
            executeVM(from, to, value, gas, gasPrice, data)

            # 1-1-4. collect refunded gas
            addBalance(delegatee, remainedGas * gasPrice)

            # 1-1-4. return
            return

        # 1-2 case where delegatee is not registered
        else:
            # "delegatee" account is in transaction but does not registered to staminaContract
            # do nothing
            assert()
            return

      # 2. normal transaction
    else:
        # 2-1. check intrinsic gas + value
        balance = getBalance(from)

        # 2-2. check intrinsic gas if `delegatee` has delegatee
        assert balance >= value + gas * gasPrice

        # 2-3. subtract gas + value
        subtractBalance(from, balance - value + gas * gasPrice)

        # 2-4. execute EVM
        executeVM(from, to, value, gas, gasPrice, data)

        # 2-5. collect refunded gas
        addBalance(from, remainedGas * gasPrice)
