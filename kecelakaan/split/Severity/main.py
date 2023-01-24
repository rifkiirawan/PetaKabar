from Severity import Severity

if __name__ == "__main__":
    severity = Severity()
    resultSeverity=severity.getKeparahanVelue()

    if (resultSeverity == "success"):
        print('Severity Success')