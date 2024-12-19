job "swamp-discord-bot" {
  datacenters = ["dc1"]
  type = "service"

  group "bot" {
    count = 1

    task "discord-bot" {
      driver = "docker"

      config {
        image = "ghcr.io/swamp-netizens/discord-bot:latest"
        force_pull = true
        logging {
          type = "journald"
          config {
            tag = "discord-bot"
          }
        }
      }

      template {
        data = <<EOH
DISCORD_TOKEN={{ with nomadVar "nomad/jobs/swamp-discord-bot" }}{{ .discord_token }}{{ end }}
EOH
        destination = "local/file.env"
        env = true
      }

      resources {
        cpu    = 200
        memory = 256
      }

      restart {
        attempts = 5
        interval = "5m"
        delay    = "25s"
        mode     = "delay"
      }
    }
  }
}
