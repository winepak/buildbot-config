#!/usr/bin/env python2

# A simplified version of builds.py from flathub
# https://github.com/flathub/buildbot-config/blob/master/builds.py

import os.path
import json
import utils

class BuildDataRepo:
    def __init__(self, name, json):
        self.name = name
        self.base = json["base"]
        self.default_branch = json.get("default-branch", "master")

class BuildDataInfo:
    def __init__(self, buildname, json, repos):
        self.buildname = buildname
        self.reponame = json.get("repo", "default")
        self.repo = repos[self.reponame]
        self.git_module = json.get("git-module", None)
        self.git_branch = json.get("git-branch", None)
        self.only_arches = json.get("only-arches", None)
	
    def get_git_branch(self):
        if self.git_branch:
            return self.git_branch
			
        return self.repo.default_branch

    def get_git_module(self):
        if self.git_module:
            return self.git_module
			
        id = util.buildname_to_id(self.buildname)
		
		return "%s.git" % id

class BuildData:
    def __init__(self, id, fp_branch):
        self.id = id
        self.fp_branch = fp_branch
        self.url = None
        self.git_branch = None

    def get_json_manifest(self):
        return "%s.json" % self.id

    def get_yaml_manifest(self):
        return "%s.yaml" % self.id

    def get_yml_manifest(self):
        return "%s.yml" % self.id

    def __str__(self):
		return "%s %s %s %s %s" % (self.id, self.fp_branch, self.url, self.git_branch, "official" if self.official else "test")

class Builds:
	def __init__(self, filename):
		self.repos = {}
		self.builds = {}
		self.default_repo = None
		
		self.load(filename)
	
	def load(self, filename):
		f = open(filename, 'r')
		config = utils.json_to_ascii(json.loads(f.read ()))
		
		for k in config["repos"]:
			r = BuildDataRepo(k, config["repos"][k])
			self.repos[k] = r
		
		for k in config["builds"]:
			i = BuildDataInfo(k, config["builds"][k], self.repos)
			self.builds[k] = i

		self.default_repo = self.repos["default"]

	def reload(self):
		self.repos = {}
		self.builds = {}
		self.default_repo = None
		
		self.load()
	
	def search(self, buildname):
		if "//" in buildname:
			split = buildname.split("//", 1)
		
		split = buildname.split("/", 1)
		
		id = split[0]
		fp_branch = None
		
		if len(split) > 1:
			fp_branch = split[1]

		if self.builds.has_key(buildname):
			info = self.builds[buildname]
			
			repo = info.repo
			module = info.get_git_module()
			git_branch = info.get_git_branch()
		else:
			if self.id_used_in_buildname(id):
				raise Exception("No defined build %s" % buildname)
				
			repo = self.default_repo
			module = "%s.git" % id
			
			if fp_branch == None:
				git_branch = repo.default_branch
			else:
				git_branch = "branch/" + fp_branch;
				
			if not util.application_id_is_valid(id):
				raise Exception("Invalid build name %s" % buildname)

		build = BuildData(id, fp_branch)
		build.url = "%s/%s" % (repo.base, module)
		build.git_branch = git_branch
		
		return build
