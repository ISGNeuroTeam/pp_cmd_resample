import pandas as pd
from scipy.signal import resample
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


class ResampleCommand(BaseCommand):
    """
    Resample signal to num samples using Fourier method along the given axis.
    | resample signal_name num=100
    """
    syntax = Syntax(
        [
            Positional("array_to_resample", required=True, otl_type=OTLType.TEXT),
            Keyword("num", required=True, otl_type=OTLType.INTEGER),
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start resample command')

        column_to_resample = self.get_arg("array_to_resample").value
        if self.get_arg("num").named_as == "":
            new_name = f"resampled_{column_to_resample}"
        else:
            new_name = self.get_arg("num").named_as
        num = self.get_arg("num").value

        self.logger.debug(f'Command resample get first positional argument = {column_to_resample}')
        self.logger.debug(f'Command resample get keyword argument = {num}')

        df = pd.DataFrame({new_name: resample(df[column_to_resample].values, num)})

        self.log_progress('Resample is complete.', stage=1, total_stages=1)

        return df
