fulltest:
	pytest -v -s --profile-svg --profile
	for i in prof/*.prof; do gprof2dot -f pstats $$i | dot -Tsvg -o $$i.svg; done

litetest:
	pytest  -m "not full" -v -s --profile-svg --profile
	for i in prof/*.prof; do gprof2dot -f pstats $$i | dot -Tsvg -o $$i.svg; done

singletest:
	cd ~/git_repos/_packages_/python/neddy
	time pytest -k "test_cl_utils" --pdb -v -s --profile-svg --profile
	for i in prof/*.prof; do gprof2dot -f pstats $$i | dot -Tsvg -o $$i.svg; done
