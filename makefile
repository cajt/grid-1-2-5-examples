FREECAD_CMD = freecadcmd
SCRIPT = scripts/export_fcstd_to_stl.py
BUILD_DIR = stl

FCSTD_FILES := $(wildcard freecad/*.FCStd)
STL_FILES := $(patsubst freecad/%.FCStd,$(BUILD_DIR)/%.stl,$(FCSTD_FILES))

all: $(BUILD_DIR) $(STL_FILES)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/%.stl: freecad/%.FCStd
	$(FREECAD_CMD) $(SCRIPT) -- $< $@

clean:
	rm -rf $(BUILD_DIR)
