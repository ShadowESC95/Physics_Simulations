# infrastructure/self-healing.nomad
job "xi-simulation" {
  group "quantum-workers" {
    reschedule {
      attempts  = 10
      interval  = "1h"
      unlimited = true
    }

    restart {
      mode = "fail"
    }
  }
}
