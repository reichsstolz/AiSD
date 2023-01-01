use std::collections::{HashSet, HashMap};
use std::io;

struct Dependency{
    name: String,
    parents: HashSet<String>,
    is_project_dep: bool
}

impl Dependency {
    fn new(name: String, is_project_dep: bool) -> Self {
        Self {
            name,
            parents: HashSet::new(),
            is_project_dep
        }
    }

    fn add_parent(&mut self, parent: &String){
        self.parents.insert(parent.clone());
    }

}


struct Graph{
    nodes: HashMap<String, Dependency>
}

impl Graph{
    fn new() -> Self {
        Self{
            nodes: HashMap::new(),
        }
    }

    fn get_path(&self, node: &Dependency, path: &mut Vec<String>){


            if  node.is_project_dep {
                print!("{}", node.name);
                for dep in path.iter().rev(){
                    print!(" ");
                    print!("{}", dep);
                }
                println!();
            }

            if node.parents.is_empty() || path.contains(&node.name){
                return;
            }

            path.push(node.name.clone());
            let mut parent_node;
            for parent_name in node.parents.iter(){
                parent_node = self.nodes.get(parent_name);
                if parent_node.is_some(){
                    self.get_path(&parent_node.unwrap(), path);
                }
            }
            path.pop();
    }

    fn get_parent(&mut self, name: &String){
        let _parent = self.nodes.get(name);
        if !_parent.is_some(){
            self.nodes.insert(name.clone(), Dependency::new(name.clone(), false));
        }
    }

    fn get_child(&mut self, name: &String, parent_name: &String, is_project: bool){
        let _child = self.nodes.get_mut(name);
        match _child {
            Some(child) => {
                child.add_parent(parent_name);
            },
            _ => {
                let mut new = Dependency::new(name.clone(), is_project);
                new.add_parent(parent_name);
                self.nodes.insert(name.clone(), new);
            }
        }
    }
}

fn main(){
    let mut vulnerable = String::new();
    let mut project_dep = String::new();
    io::stdin().read_line(&mut vulnerable).unwrap();
    io::stdin().read_line(&mut project_dep).unwrap();
    let vuln_vec = vulnerable.split(" ").map(|x| x.to_owned()).collect::<Vec<String>>();
    let project_dep_vec = project_dep.split(" ").map(|x| x.to_owned()).collect::<Vec<String>>();

    let mut graph = Graph::new();

    for dep in project_dep_vec.iter(){
        graph.get_child(dep, &"project".to_string(), true);
    }

    let mut dep_vec: Vec<String>;
    for line in io::stdin().lines() {

        dep_vec = line.unwrap().split(" ").map(|x| x.to_owned()).collect::<Vec<String>>();
        graph.get_parent(&dep_vec[0]);
        for i in 1..dep_vec.len(){
            graph.get_child(&dep_vec[i], &dep_vec[0], false);
        }
    }
    let mut vuln;
    for vuln_name in vuln_vec.iter(){
        vuln = graph.nodes.get(vuln_name);
        if vuln.is_some(){
            graph.get_path(vuln.unwrap(),&mut Vec::new());
        }
    }

}