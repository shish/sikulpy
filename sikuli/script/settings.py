from typing import List


class Settings(object):
    autoWaitTimeout = 0

    Scale = 1  # FIXME: unofficial
    Channel = None  # FIXME: unofficial

    ImagePaths = []  # type: List[str]

    # Either option might be switched on (True) or off (False), to show or
    # hide the respective message type in the IDE console or on command line
    # ([log], [info], [debug]).
    ActionLogs = False
    InfoLogs = False
    DebugLogs = False

    # The default minimum similarity of find operations. While using a
    # Region.find() operation, if only an image file is provided, Sikuli
    # searches the region using a default minimum similarity of 0.7.
    MinSimilarity = 0.7

    # Control the time taken for mouse movement to a target location by
    # setting this value to a decimal value (default 0.5). The unit is
    # seconds. Setting it to 0 will switch off any animation (the mouse will
    # "jump" to the target location).
    MoveMouseDelay = 0.5

    # move -> mouse down -> move (drag) -> mouse up (drop)
    DelayBeforeMouseDown = 0.1
    DelayBeforeDrag = 0.1
    DelayBeforeDrop = 0.1

    # Control the duration of the visual effect (seconds).
    SlowMotionDelay = 2.0

    # Specify the number of times actual search operations are performed per
    # second while waiting for a pattern to appear or vanish.
    # As a standard behavior Sikuli internally processes about 3 search
    # operations per second, when processing a Region.wait(), Region.exists(),
    # Region.waitVanish(), Region.observe()). In cases where this leads to an
    # excessive usage of system resources or if you intentionally want to
    # look for the visual object not so often, you may set the respective
    # values to what you need. Since the value is used as a rate per second,
    # specifying values between 1 and near zero, leads to scans every x
    # seconds (e.g. specifying 0.5 will lead to scans every 2 seconds):
    WaitScanRate = 3.0
    ObserveScanRate = 3.0

    # The minimum size in pixels of a change to trigger a change event when
    # using Region.onChange() without specifying this value. The default
    # value is 50.
    ObserveMinChangedPixels = 50
