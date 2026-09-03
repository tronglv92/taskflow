<template>
  <div class="about">
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">About TaskFlow</h2>

        <div class="prose max-w-none">
          <p class="text-gray-700 mb-4">
            TaskFlow is the reference application for the Platform Engineering Bootcamp
            by TeKanAid Academy. Throughout the 20-week bootcamp, you'll build this
            application from scratch, learning industry-standard platform engineering
            practices.
          </p>

          <h3 class="text-xl font-semibold text-gray-900 mt-6 mb-3">
            What You'll Build
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div class="bg-blue-50 p-4 rounded-lg">
              <h4 class="font-semibold text-gray-900 mb-2">Weeks 1-6: Foundation</h4>
              <ul class="text-sm text-gray-700 space-y-1">
                <li>• FastAPI backend with REST API</li>
                <li>• Vue.js frontend with routing</li>
                <li>• PostgreSQL database</li>
                <li>• Docker containerization</li>
              </ul>
            </div>

            <div class="bg-green-50 p-4 rounded-lg">
              <h4 class="font-semibold text-gray-900 mb-2">Weeks 7-12: Infrastructure</h4>
              <ul class="text-sm text-gray-700 space-y-1">
                <li>• Kubernetes deployment</li>
                <li>• Terraform infrastructure</li>
                <li>• CI/CD pipelines</li>
                <li>• Service mesh (Consul)</li>
              </ul>
            </div>

            <div class="bg-purple-50 p-4 rounded-lg">
              <h4 class="font-semibold text-gray-900 mb-2">Weeks 13-18: Advanced</h4>
              <ul class="text-sm text-gray-700 space-y-1">
                <li>• Python automation</li>
                <li>• Crossplane for IaC</li>
                <li>• GitOps with ArgoCD</li>
                <li>• Full observability</li>
              </ul>
            </div>

            <div class="bg-yellow-50 p-4 rounded-lg">
              <h4 class="font-semibold text-gray-900 mb-2">Weeks 19-20: Production</h4>
              <ul class="text-sm text-gray-700 space-y-1">
                <li>• Multi-environment deployment</li>
                <li>• Security hardening</li>
                <li>• Performance optimization</li>
                <li>• Complete portfolio project</li>
              </ul>
            </div>
          </div>

          <h3 class="text-xl font-semibold text-gray-900 mt-6 mb-3">
            Technology Stack
          </h3>

          <div class="bg-gray-50 p-4 rounded-lg">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <p class="font-semibold text-gray-900">Backend</p>
                <p class="text-gray-600">Python FastAPI</p>
              </div>
              <div>
                <p class="font-semibold text-gray-900">Frontend</p>
                <p class="text-gray-600">Vue.js 3 + Pinia</p>
              </div>
              <div>
                <p class="font-semibold text-gray-900">Database</p>
                <p class="text-gray-600">PostgreSQL</p>
              </div>
              <div>
                <p class="font-semibold text-gray-900">Container</p>
                <p class="text-gray-600">Docker</p>
              </div>
              <div>
                <p class="font-semibold text-gray-900">Orchestration</p>
                <p class="text-gray-600">Kubernetes</p>
              </div>
              <div>
                <p class="font-semibold text-gray-900">IaC</p>
                <p class="text-gray-600">Terraform/Crossplane</p>
              </div>
              <div>
                <p class="font-semibold text-gray-900">CI/CD</p>
                <p class="text-gray-600">GitHub Actions/ArgoCD</p>
              </div>
              <div>
                <p class="font-semibold text-gray-900">Monitoring</p>
                <p class="text-gray-600">Prometheus/Grafana</p>
              </div>
            </div>
          </div>

          <h3 class="text-xl font-semibold text-gray-900 mt-6 mb-3">
            Current Version
          </h3>

          <p class="text-gray-700">
            <strong>Version:</strong> 0.6.0 (Backend + frontend reading reference)<br>
            <strong>Status:</strong> Development
          </p>

          <div class="mt-6 bg-blue-100 border-l-4 border-blue-500 p-4">
            <p class="text-sm text-blue-700">
              <strong>💡 Tip:</strong> This application evolves throughout the bootcamp.
              Each week introduces new features, technologies, and platform engineering concepts.
              Your final version will be a production-ready application worthy of your GitHub portfolio!
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No script needed for static about page
</script>
