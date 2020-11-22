import pandas as pd
import yahoofinancials

def get_company_financial(symbol = 'NaN',frequency = 'annual',statement_type = ['balance', 'income', 'cash']):
    
    if symbol == "NaN":
        return 'please input symbol'

    df = pd.DataFrame()
    try :
        stk = yahoofinancials.YahooFinancials(symbol) 
    except TypeError:
        return 'please input symbol'
        
    subject_list = list(stk.get_financial_stmts(frequency, statement_type).keys())

    for subject in subject_list:
        globals()['df_'+subject] = pd.DataFrame()
        try:
            data = stk.get_financial_stmts(frequency, statement_type)[subject][symbol]
        except KeyError :
            return 'please input symbol'

        for num in range(len(data)):
            date_col = list(data[num].keys())[0]
            data[num][date_col]['date'] = date_col
            globals()['df_'+subject] = globals()['df_'+subject].append(pd.DataFrame([data[num][date_col]]),ignore_index=True)

    if frequency != 'quarterly':
        if len(statement_type) == 3:
            df = pd.concat([df_balanceSheetHistory,df_cashflowStatementHistory,df_incomeStatementHistory], axis=1)
        elif len(statement_type) == 2:
            if 'balance' not in statement_type:
                df = pd.concat([df_cashflowStatementHistory,df_incomeStatementHistory], axis=1)
            elif 'income' not in statement_type:
                df = pd.concat([df_balanceSheetHistory,df_cashflowStatementHistory], axis=1)
            else:
                df = pd.concat([df_balanceSheetHistory,df_incomeStatementHistory], axis=1)
        else:
            if 'balance' in statement_type:
                df = df_balanceSheetHistory
            elif 'income' in statement_type:
                df = df_incomeStatementHistory
            else:
                df = df_cashflowStatementHistory
    else:
        if len(statement_type) == 3:
            df = pd.concat([df_balanceSheetHistoryQuarterly,df_cashflowStatementHistoryQuarterly,df_incomeStatementHistoryQuarterly], axis=1)
        elif len(statement_type) == 2:
            if 'balance' not in statement_type:
                df = pd.concat([df_cashflowStatementHistoryQuarterly,df_incomeStatementHistoryQuarterly], axis=1)
            elif 'income' not in statement_type:
                df = pd.concat([df_balanceSheetHistoryQuarterly,df_cashflowStatementHistoryQuarterly], axis=1)
            else:
                df = pd.concat([df_balanceSheetHistoryQuarterly,df_incomeStatementHistoryQuarterly], axis=1)
        else:
            if 'balance' in statement_type:
                df = df_balanceSheetHistoryQuarterly
            elif 'income' in statement_type:
                df = df_incomeStatementHistoryQuarterly
            else:
                df = df_cashflowStatementHistoryQuarterly
    
    return df

