.PHONY: all
all: clean songs.db

songs.db: src/create_tables.py
	rm -rf $@
	$<

.PHONY: clean
clean:
	rm -f songs.db
