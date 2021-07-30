from common.benchmark_wrapper import BenchmarkWrapper
import json
import subprocess
import os
import json


class BlenderBenchmark(BenchmarkWrapper):

    """
    This is a Blender benchmark implementation.
    """

    def __init__(self):
        self._settings = {}
        self.filePath = os.path.dirname(__file__)
        self.baseCommand = "bin/benchmark-launcher-cli"

    def setSettings(self, settings_file):
        self._settings = json.load(open(settings_file, "r"))

    def startBenchmark(self, verbosity=None):
        self.getSettings(("blender", "download"))
        self.getSettings(("scenes", "download"))
        self.scenes = " ".join([str(elem) for elem in self._settings["scenes"]])
        self.verbosity = verbosity
        if self.verbosity == None:
            self.verbosity = self._settings["verbosity"]

        try:
            startBench = subprocess.run(
                [
                    os.path.join(self.filePath, self.baseCommand),
                    "benchmark",
                    str(self.scenes),
                    "-b",
                    str(self._settings["blender_version"]),
                    "--device-type",
                    str(self._settings["device_type"]),
                    "--json",
                    "-v",
                    str(self.verbosity),
                ],stdout=subprocess.PIPE

            )
        except subprocess.CalledProcessError as e:
            print(e.output)
            exit
        if startBench.returncode != 0:
            return startBench.stderr
        else:
            s = startBench.stdout.decode("utf-8")
            s = s[4:-2].replace('false','False')
            s = eval(s)
            returnDict = {}
            specs = ["timestamp","stats","blender_version","benchmark_launcher","benchmark_script","scene"]
            for spec in specs:
                returnDict[spec] = s.get(spec,None)
            return returnDict

    def benchmarkStatus():
        pass

    def getSettings(self, args):
        commands = {
            "blender": {  # Container Dictionary for blender download managerc
                "download": [  # Downloads the blender version specified in the settings
                    os.path.join(self.filePath, self.baseCommand),
                    "blender",
                    "download",
                    str(self._settings["blender_version"]),
                ],
                "list": [  # Lists available blender versions
                    os.path.join(self.filePath, self.baseCommand),
                    "blender",
                    "list",
                ],
            },
            "devices": [  # Prints compatible devices
                os.path.join(self.filePath, self.baseCommand),
                "devices",
                "-b",
                str(self._settings["blender_version"]),
            ],
            "help": [  # Prints the help window
                os.path.join(self.filePath, self.baseCommand),
                "--help",
            ],
            "scenes": {  # Container Dictionary for scenes download manager
                "download": [  # Downloads the scenes mentioned in settings
                    os.path.join(self.filePath, self.baseCommand),
                    "scenes",
                    "download",
                    "-b",
                    str(self._settings["blender_version"]),
                ]
                + (self._settings["scenes"]),
                "list": [  # Lists scenes
                    os.path.join(self.filePath, self.baseCommand),
                    "scenes",
                    "list",
                    "-b",
                    str(self._settings["blender_version"]),
                ],
            },
            "clear_cache": [  # Clears cache generated by the blender cli
                os.path.join(self.filePath, self.baseCommand),
                "clear_cache",
            ],
        }
        if len(args) == 2:
            if args[1] == "help" or args[1] == "--help":
                command = [os.path.join(self.filePath, self.baseCommand)] + [
                    args[0],
                    "help",
                ]
            else:
                command = commands.get(args[0]).get(args[1])
        elif len(args) == 1:
            command = commands.get(args[0])
        else:
            raise Exception("Please check your command and enter again")
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
        except KeyError as e:
            print(e.output)
        if args[0] == "devices":
            p2 = subprocess.Popen(
                ["grep","-wv", "CPU"], stdin=process.stdout, stdout=subprocess.PIPE
            )
            process.stdout.close()
            print(p2.communicate()[0].decode())
        else:
            print(process.communicate()[0].decode())

    def stopBenchmark():
        pass

