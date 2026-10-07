nextflow.enable.dsl=2

params.input = "config/samplesheet.csv"
params.outdir = "results"
params.genome = "GATK.GRCh38"
params.sarek = "3.10.0"

workflow {
    log.info "Project 07 — WES | GSE179296 | nf-core/sarek ${params.sarek} | ${params.genome}"

    // Production command:
    // nextflow run nf-core/sarek -r 3.10.0 -profile docker \
    //   --input config/samplesheet.csv --outdir results \
    //   --genome GATK.GRCh38 --wes --tools mutect2,vep

    Channel.of(params.input).view { "Input samplesheet: $it" }
}
