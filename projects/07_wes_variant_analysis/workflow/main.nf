nextflow.enable.dsl=2

params.samplesheet = "config/samplesheet.csv"

process QC {
    tag '$sample_id'
    input:
    tuple val(sample_id), path(reads)

    output:
    path 'fastqc', emit: fastqc

    script:
    """
    mkdir -p fastqc
    fastqc -o fastqc $reads[0] $reads[1]
    """
}

process ALIGN {
    tag '$sample_id'
    input:
    tuple val(sample_id), path(reads)

    output:
    tuple val(sample_id), path('*.bam'), emit: bam

    script:
    """
    bwa-mem2 mem -t $task.cpus reference.fa $reads[0] $reads[1] |
      samtools sort -@ $task.cpus -o $sample_id.bam
    samtools index $sample_id.bam
    """
}

workflow {
    reads = Channel
        .fromPath(params.samplesheet)
        .splitCsv(header: true)
        .map { row -> tuple(row.sample_id, [file(row.fastq_1), file(row.fastq_2)]) }

    QC(reads)
    ALIGN(reads)
}
