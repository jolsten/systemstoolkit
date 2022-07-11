<<<<<<< HEAD
import datetime
import numpy as np
from typing import Union, Optional, Tuple
from numpy.typing import ArrayLike

DateTimeLike = Union[datetime.datetime, np.datetime64]
DateTimeArrayLike = ArrayLike

TimeInstant = Union[str, datetime.datetime]
TimeInterval = Union[str, Tuple[TimeInstant, TimeInstant]]
=======
import datetime
import numpy as np
from typing import Union
from numpy.typing import ArrayLike

DateTimeLike = Union[datetime.datetime, np.datetime64]
DateTimeArrayLike = ArrayLike
>>>>>>> 35a54389bd7199e199d4593870c92d2e6095ccf4
