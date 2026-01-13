# CI/CD Documentation

This document describes the Continuous Integration and Continuous Deployment (CI/CD) workflows configured for the Resonance School project.

## Workflows

### 1. Lint Workflow (`.github/workflows/lint.yml`)

**Triggers:**
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`

**Jobs:**
- **lint-html**: Validates HTML files using `html-validate` and `tidy`
- **lint-shell**: Validates shell scripts using `shellcheck`

**Purpose:** Ensures code quality and catches syntax errors early in the development process.

### 2. Test Workflow (`.github/workflows/test.yml`)

**Triggers:**
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`

**Jobs:**
- **test-html**: Validates HTML structure and readability
- Tests shell script syntax validation

**Purpose:** Validates that all files are properly structured and executable.

### 3. Docker Build Workflow (`.github/workflows/docker-build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual trigger via `workflow_dispatch`

**Jobs:**
- **docker**: Builds Docker image for the web application
- Uses Docker Buildx for optimized builds
- Includes caching for faster builds

**Purpose:** Ensures the application can be successfully containerized and deployed.

### 4. Sync Common Core Workflow (`.github/workflows/sync-common-core.yml`)

**Triggers:**
- Repository dispatch event: `common-core-update`
- Manual trigger via `workflow_dispatch`
- Scheduled daily at 2 AM UTC

**Jobs:**
- **sync-common-core**: Checks for updates from the common-core repository
- Creates pull requests when synchronization is needed

**Purpose:** Maintains alignment with shared modules from the common-core repository.

### 5. Sync Partners Documentation (`.github/workflows/sync-partners-doc.yml`)

**Triggers:**
- Push to `main` branch when `README_PARTNERS.md` changes
- Manual trigger via `workflow_dispatch`

**Jobs:**
- **sync-partners-doc**: Synchronizes `README_PARTNERS.md` with the LexAmoris repository

**Purpose:** Keeps partner documentation in sync across related repositories.

## Docker Support

### Dockerfile

The project includes a production-ready Dockerfile that:
- Uses `nginx:alpine` as the base image for minimal size
- Copies HTML files and documentation
- Configures nginx with security headers
- Includes health checks
- Exposes port 80

### docker-compose.yml

For local development:
```bash
docker-compose up -d
```

Access the application at `http://localhost:8080`

### Building Manually

```bash
# Build the image
docker build -t resonance-school:latest .

# Run the container
docker run -d -p 8080:80 --name resonance resonance-school:latest

# View logs
docker logs resonance

# Stop the container
docker stop resonance
```

## Configuration Files

### .gitignore

Excludes common artifacts:
- Node modules
- Build directories
- IDE files
- Temporary files
- Environment files

### .dockerignore

Optimizes Docker builds by excluding:
- Git metadata
- CI/CD workflows
- Old file versions
- Development files
- IDE configurations

## Security

All workflows include:
- Automated dependency updates via Dependabot (recommended)
- Security scanning for Docker images (recommended to add)
- YAML syntax validation
- Shell script linting

## Best Practices

1. **Always run workflows locally when possible** before pushing
2. **Use feature branches** for development
3. **Keep workflows minimal** - only test what's necessary
4. **Cache dependencies** to speed up builds
5. **Use semantic versioning** for releases

## Monitoring

GitHub Actions provide:
- Build status badges (can be added to README.md)
- Email notifications on failures
- Workflow run history
- Job logs for debugging

## Future Enhancements

Potential improvements:
- [ ] Add automated deployment to staging/production
- [ ] Implement semantic release automation
- [ ] Add performance testing
- [ ] Add dependency vulnerability scanning
- [ ] Add container image scanning
- [ ] Implement automated changelog generation
