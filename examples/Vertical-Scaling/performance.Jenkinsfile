node {
    def legion = load legion()

    legion.pod(ram: '10Gi') {
        stage('System info'){
            sh "df -h"
            sh "cat /proc/cpuinfo"
            sh "free -g"
        }
    }
}
