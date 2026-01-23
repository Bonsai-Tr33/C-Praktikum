import pandas as pd
import math
import numpy as np

class Messreihe:
    def __init__(self, filepath, N1, N2, R=0.2, F=0.9, k=0.1):           # Loading CSV
        self.N1 = N1
        self.N2 = N2
        self.filepath = filepath
        self.data = pd.read_csv(filepath)
        second = self.data.columns[1]
        third = self.data.columns[2]

        self.data[second] = self.data[second].apply(lambda x: self.H(x, self.N1, R))
        self.data[third] = self.data[third].apply(lambda x: self.B(x, self.N2, F, k))
        self.data.columns = ['Time (s)','H(A/m)', 'B(T)']

    def H(self, U, N1, R):
        dm = 0.24
        return (N1*U)/(math.pi*dm*R)

    def B(self, U, N2, F, k):
        da = 0.26
        di = 0.22
        h = 0.03
        k = 0.1
        return U* k / (N2*(F*h*(da-di)/2))

    def dataArray(self):
        return self.data

    def show_head(self, n=5):               # Show first n Data frames
        return self.data.head(n)
    
    import numpy as np

    def hysteresis_drift_from_arrays(time, x, y, x_tolerance=1e-4):
        """
        Driftanalyse eines Hystereseversuchs.

        Parameter
        ---------
        time : np.ndarray
            Zeitarray
        x : np.ndarray
            Magnetisierungsgröße (z.B. Feld, Spannung)
        y : np.ndarray
            Messsignal
        x_tolerance : float
            Toleranz für das Wiederfinden desselben x-Wertes im Rücklauf

        Returns
        -------
        dict mit:
            t_max, x_max, y_max
            t_return, x_return, y_return
            drift, delta_t
        """

        time = np.asarray(time)
        x = np.asarray(x)
        y = np.asarray(y)

        # -----------------------------
        # 1) Maximum der Aufmagnetisierung
        # -----------------------------
        max_idx = np.argmax(x)

        t_max = time[max_idx]
        x_max = x[max_idx]
        y_max = y[max_idx]

        # -----------------------------
        # 2) Rücklauf: gleicher x-Wert
        # -----------------------------
        x_after = x[max_idx + 1:]
        time_after = time[max_idx + 1:]
        y_after = y[max_idx + 1:]

        diff = np.abs(x_after - x_max)
        valid = np.where(diff <= x_tolerance)[0]

        if len(valid) == 0:
            raise ValueError(
                "Kein Rücklaufpunkt mit passendem x-Wert gefunden. "
                "x_tolerance erhöhen oder interpolieren."
            )

        # erster Treffer im Rücklauf
        idx_return = valid[0]

        t_return = time_after[idx_return]
        x_return = x_after[idx_return]
        y_return = y_after[idx_return]

        # -----------------------------
        # 3) Drift & Zeitabstand
        # -----------------------------
        drift = y_return - y_max
        delta_t = t_return - t_max

        return {
            "t_max": t_max,
            "x_max": x_max,
            "y_max": y_max,
            "t_return": t_return,
            "x_return": x_return,
            "y_return": y_return,
            "drift": drift,
            "delta_t": delta_t
        }
