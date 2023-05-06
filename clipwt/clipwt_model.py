from dataclasses import dataclass
from clipwt.clipwt_constants import ClipAppStatus

@dataclass
class ClipWtModel:

    status : ClipAppStatus
    content : str
    old_content : str
