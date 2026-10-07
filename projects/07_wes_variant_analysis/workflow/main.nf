nextflow.enable.dsl=2

params.input = "config/samplesheet.csv"
params.outdir = "results"
params.genome = "GATK.GRCh38"
params.sarek = "3.10.0"

workflow {
    log.info "Project 07 — WES | GSE179296 | nf-core/sarek $\{params.sarek\} | $\{params.genome\}"
    log.info "Production execution is pinned to nf-core/sarek $\{params.sarek\}."

    /*
     * This repository workflow is intentionally a thin entry point.
     * Run the pinned nf-core/sarek release through scripts/run_sarek.sh.
     * Keeping Sarek as the upstream workflow avoids duplicating a large
     * production pipeline in this portfolio repository.
     */
    Channel.of(params.input).view { "Sarek samplesheet: $it" }
}
