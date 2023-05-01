try:
    from .._data import prepare_data
    import arcgis as ag
    from fastai.basic_train import LearnerCallback
    import traceback
    from typing import List
    import random
    import time
    import os
    import psutil
    import torch
    import gc
    from time import sleep
    from IPython.display import clear_output
    import threading
    import functools
    import time
    import importlib

    HAS_FASTAI = True
except Exception as e:
    print(e)
    import_exception = "\n".join(
        traceback.format_exception(type(e), e, e.__traceback__)
    )
    HAS_FASTAI = False


class ToolIsCancelled(Exception):
    pass


class train_callback(LearnerCallback):
    def __init__(self, learn, stop_var):
        self.counter = 0
        self.stop_var = stop_var
        super().__init__(learn)

    def on_batch_end(self, **kwargs):
        # print(self.counter)
        self.counter += 1
        is_present = importlib.util.find_spec("arcpy")
        if is_present is not None:
            import arcpy

            if arcpy.env.isCancelled:
                raise ToolIsCancelled("Function aborted by User.")
        if self.counter > self.stop_var:
            self.counter = 0
            return {"stop_epoch": True}


def synchronized(wrapped):
    lock = threading.Lock()

    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            result = wrapped(*args, **kwargs)
            clear_output(wait=True)
            return result

    return _wrap


class EvaluateBatchSize:
    def __init__(self, model, path, batch_size, dataset_type, **kwargs):
        self.model = model
        self.batch_size = batch_size
        self.data = None
        self.is_completed = False
        self.is_executing = False
        self.dataset_type = dataset_type
        self.path = path
        self.wait = True
        self.lr_val = None
        self.is_mm = False
        self.command = {"stop_thread": False}
        if "model_name" in kwargs:
            self.is_mm = True
            self.model_name = kwargs["model_name"]

    @synchronized
    def get_batch_size(self, name: str):
        try:
            print(f"{name}.")
            while self.command["stop_thread"] is False:
                model, lr_val, data = None, None, None
                try:
                    is_present = importlib.util.find_spec("arcpy")
                    if is_present is not None:
                        import arcpy

                        if arcpy.env.isCancelled:
                            raise ToolIsCancelled("Function aborted by User.")
                    if self.is_executing == False:
                        self.is_executing = True
                        self.data = prepare_data(
                            self.path,
                            batch_size=self.batch_size,
                            dataset_type=self.dataset_type,
                        )
                        if not self.is_mm:
                            model = getattr(ag.learn, self.model)(self.data)
                        else:
                            if self.model_name == "CascadeRCNN":
                                model = getattr(ag.learn, self.model)(
                                    self.data, model="cascade_rcnn"
                                )
                            elif self.model_name == "CascadeRPN":
                                model = getattr(ag.learn, self.model)(
                                    self.data, model="cascade_rpn"
                                )
                            else:
                                model = getattr(ag.learn, self.model)(
                                    self.data, model=self.model_name.lower()
                                )

                        lr_val = model.lr_find(allow_plot=False)
                        self.wait = False
                        self.lr_val = lr_val
                        self.is_completed = True
                        del model
                        gc.collect()
                        torch.cuda.empty_cache()
                        return
                    self.is_executing = False
                except Exception as E:
                    if "CUDA out of memory" in str(E):
                        print("Out of memory with batch size:", self.batch_size)
                        self.is_completed = False
                        del model
                        model = None
                        gc.collect()
                        torch.cuda.empty_cache()
                        self.is_completed = False
                        self.is_executing = False
                        self.command["stop_thread"] = True
                        clear_output(wait=True)
                        continue
                    else:
                        self.wait = False
                        return None, None, None
                finally:
                    gc.collect()
                    torch.cuda.empty_cache()
            else:
                gc.collect()
                torch.cuda.empty_cache()
                if (not self.is_completed) and (self.is_executing == False):
                    self.command["stop_thread"] = False
                    self.batch_size = int(self.batch_size // 2)
                    if self.batch_size >= 2:
                        self.start_thread(
                            "New thread initiated for batch size: "
                            + str(self.batch_size)
                        )
                    else:
                        self.wait = False
                        return None, None, None
                return
        except Exception as e:
            self.wait = False
            print("Error: ")
            print(e)
            return None, None

        print(f"Exiting.")

    def start_thread(self, name: str):
        threading.Thread(target=self.get_batch_size, args=(name,), daemon=True).start()

    def wait_until(self):
        while self.wait:
            sleep(10)
        else:
            return self.batch_size, self.lr_val, self.data
