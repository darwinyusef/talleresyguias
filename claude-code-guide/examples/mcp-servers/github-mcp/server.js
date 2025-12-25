/**
 * GitHub MCP Server
 * Permite a Claude Code interactuar con GitHub API
 */

const { MCPServer } = require('@anthropic-ai/mcp-sdk');
const { Octokit } = require('@octokit/rest');
const express = require('express');

class GitHubMCPServer {
  constructor(port = 3000) {
    this.port = port;
    this.octokit = new Octokit({
      auth: process.env.GITHUB_TOKEN
    });

    this.server = new MCPServer({
      name: 'github-mcp',
      version: '1.0.0',
      description: 'GitHub integration for Claude Code'
    });

    this.setupTools();
  }

  setupTools() {
    // Tool: List repositories
    this.server.addTool({
      name: 'list_repos',
      description: 'List user repositories',
      parameters: {
        type: 'object',
        properties: {
          username: {
            type: 'string',
            description: 'GitHub username'
          },
          type: {
            type: 'string',
            enum: ['all', 'owner', 'member'],
            description: 'Filter by repository type'
          },
          sort: {
            type: 'string',
            enum: ['created', 'updated', 'pushed', 'full_name'],
            description: 'Sort order'
          }
        },
        required: ['username']
      },
      handler: async ({ username, type = 'owner', sort = 'updated' }) => {
        try {
          const { data } = await this.octokit.repos.listForUser({
            username,
            type,
            sort,
            per_page: 100
          });

          return {
            success: true,
            count: data.length,
            repositories: data.map(repo => ({
              name: repo.name,
              full_name: repo.full_name,
              description: repo.description,
              private: repo.private,
              url: repo.html_url,
              stars: repo.stargazers_count,
              forks: repo.forks_count,
              language: repo.language,
              updated_at: repo.updated_at
            }))
          };
        } catch (error) {
          return {
            success: false,
            error: error.message
          };
        }
      }
    });

    // Tool: Get repository info
    this.server.addTool({
      name: 'get_repo_info',
      description: 'Get detailed information about a repository',
      parameters: {
        type: 'object',
        properties: {
          owner: {
            type: 'string',
            description: 'Repository owner'
          },
          repo: {
            type: 'string',
            description: 'Repository name'
          }
        },
        required: ['owner', 'repo']
      },
      handler: async ({ owner, repo }) => {
        try {
          const { data } = await this.octokit.repos.get({ owner, repo });

          return {
            success: true,
            repository: {
              name: data.name,
              full_name: data.full_name,
              description: data.description,
              private: data.private,
              url: data.html_url,
              stars: data.stargazers_count,
              watchers: data.watchers_count,
              forks: data.forks_count,
              open_issues: data.open_issues_count,
              language: data.language,
              topics: data.topics,
              created_at: data.created_at,
              updated_at: data.updated_at,
              default_branch: data.default_branch,
              license: data.license?.name
            }
          };
        } catch (error) {
          return {
            success: false,
            error: error.message
          };
        }
      }
    });

    // Tool: List pull requests
    this.server.addTool({
      name: 'list_pull_requests',
      description: 'List pull requests in a repository',
      parameters: {
        type: 'object',
        properties: {
          owner: { type: 'string' },
          repo: { type: 'string' },
          state: {
            type: 'string',
            enum: ['open', 'closed', 'all'],
            description: 'Filter by state'
          }
        },
        required: ['owner', 'repo']
      },
      handler: async ({ owner, repo, state = 'open' }) => {
        try {
          const { data } = await this.octokit.pulls.list({
            owner,
            repo,
            state,
            per_page: 50
          });

          return {
            success: true,
            count: data.length,
            pull_requests: data.map(pr => ({
              number: pr.number,
              title: pr.title,
              state: pr.state,
              author: pr.user.login,
              created_at: pr.created_at,
              updated_at: pr.updated_at,
              url: pr.html_url,
              draft: pr.draft,
              mergeable: pr.mergeable,
              labels: pr.labels.map(l => l.name)
            }))
          };
        } catch (error) {
          return {
            success: false,
            error: error.message
          };
        }
      }
    });

    // Tool: Create issue
    this.server.addTool({
      name: 'create_issue',
      description: 'Create a new issue in a repository',
      parameters: {
        type: 'object',
        properties: {
          owner: { type: 'string' },
          repo: { type: 'string' },
          title: { type: 'string' },
          body: { type: 'string' },
          labels: {
            type: 'array',
            items: { type: 'string' }
          },
          assignees: {
            type: 'array',
            items: { type: 'string' }
          }
        },
        required: ['owner', 'repo', 'title']
      },
      handler: async ({ owner, repo, title, body, labels, assignees }) => {
        try {
          const { data } = await this.octokit.issues.create({
            owner,
            repo,
            title,
            body,
            labels,
            assignees
          });

          return {
            success: true,
            issue: {
              number: data.number,
              title: data.title,
              url: data.html_url,
              state: data.state
            }
          };
        } catch (error) {
          return {
            success: false,
            error: error.message
          };
        }
      }
    });

    // Tool: Search code
    this.server.addTool({
      name: 'search_code',
      description: 'Search code across GitHub',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'Search query (e.g., "MLflow repo:owner/repo")'
          },
          per_page: {
            type: 'number',
            description: 'Results per page (max 100)'
          }
        },
        required: ['query']
      },
      handler: async ({ query, per_page = 30 }) => {
        try {
          const { data } = await this.octokit.search.code({
            q: query,
            per_page
          });

          return {
            success: true,
            total_count: data.total_count,
            items: data.items.map(item => ({
              name: item.name,
              path: item.path,
              repository: item.repository.full_name,
              url: item.html_url
            }))
          };
        } catch (error) {
          return {
            success: false,
            error: error.message
          };
        }
      }
    });
  }

  start() {
    const app = express();

    // Health check
    app.get('/health', (req, res) => {
      res.json({ status: 'healthy', service: 'github-mcp' });
    });

    // MCP endpoints
    app.use(this.server.middleware());

    app.listen(this.port, () => {
      console.log(`GitHub MCP Server listening on port ${this.port}`);
      console.log(`Health check: http://localhost:${this.port}/health`);
    });
  }
}

// Start server
if (require.main === module) {
  const server = new GitHubMCPServer(process.env.PORT || 3000);
  server.start();
}

module.exports = GitHubMCPServer;
