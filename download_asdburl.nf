nextflow.enable.dsl=2

process as_dwld{
	maxForks=3
	errorStrategy { sleep(Math.pow(2, task.attempt) * 100 as long); return 'retry'}
	maxRetries 3
	publishDir "./asdb_gbk/",
		mode: 'copy',
		overwrite: false
	label="downld"
	conda "download_asdb.yml" 

	input:
		path x
	output:
		path '*.gbk'
		path '*.tsv'

	script:
	"""
	python /Users/jfgarcia/scilife/asdb_v3/download_asdburl.py ${x}
	"""
	}

workflow{
	data=channel.fromPath('asdb_url/*')
	as_dwld(data)
	}
