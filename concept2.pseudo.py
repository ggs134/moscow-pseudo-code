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

# "delegatee" is optional in transaction
def tx_execute_after(from, to, value, gasLimit, gasPrice, data, delegatee=none):
    # 1. check if delegatee passed or not
    if delegatee:
        # 1-1. check if delegatee account registered in staminaContract, executeVM
        if (staminaContract.isDelegatee(delegatee)):

            # 1-1-1. check intrinsic gas if `delegatee` has delegatee
            assert staminaContract.balanceOf(delegatee) >= gasLimit * gasPrice

            # 1-1-2. substract gas from delegatee
            staminaContract.substractBalance(delegatee, gasLimit * gasPrice)

            # 1-1-3. execute EVM
            executeVM(from, to, value, gasLimit, gasPrice, data)

            # 1-1-4. collect refunded gas
            addBalance(delegatee, gasRemained * gasPrice)

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
        return tx_execute_before(from, to, value, gasLimit, gasPrice, data)
