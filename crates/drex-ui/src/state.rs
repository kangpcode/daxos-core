//! ============================================================================
//! DAXOS DREX-UI DECLARATIVE FRAMEWORK: REACTIVE STATE MODEL
//! File: crates/drex-ui/src/state.rs
//! Purpose: Reactive state, two-way bindings, observable objects, and environment store
//! Compatible with SwiftUI & HarmonyOS ArkUI paradigm
//! ============================================================================

use std::any::{Any, TypeId};
use std::collections::HashMap;
use std::sync::{Arc, Mutex, RwLock};

// ----------------------------------------------------------------------------
// 1. STATE & TWO-WAY BINDINGS (SwiftUI @State / ArkUI @State)
// ----------------------------------------------------------------------------

#[derive(Clone)]
pub struct State<T> {
    inner: Arc<Mutex<T>>,
    listeners: Arc<Mutex<Vec<Arc<dyn Fn(&T) + Send + Sync>>>>,
}

impl<T: Clone + 'static> State<T> {
    pub fn new(val: T) -> Self {
        Self {
            inner: Arc::new(Mutex::new(val)),
            listeners: Arc::new(Mutex::new(Vec::new())),
        }
    }

    pub fn get(&self) -> T {
        self.inner.lock().unwrap().clone()
    }

    pub fn set(&self, new_val: T) {
        {
            let mut lock = self.inner.lock().unwrap();
            *lock = new_val.clone();
        }
        let list = self.listeners.lock().unwrap();
        for listener in list.iter() {
            listener(&new_val);
        }
    }

    pub fn binding(&self) -> Binding<T> {
        Binding {
            state: self.clone(),
        }
    }

    pub fn on_change<F>(&self, callback: F)
    where
        F: Fn(&T) + Send + Sync + 'static,
    {
        let mut list = self.listeners.lock().unwrap();
        list.push(Arc::new(callback));
    }
}

// ----------------------------------------------------------------------------
// 2. BINDING (SwiftUI @Binding / ArkUI @Link)
// ----------------------------------------------------------------------------

#[derive(Clone)]
pub struct Binding<T> {
    state: State<T>,
}

impl<T: Clone + 'static> Binding<T> {
    pub fn get(&self) -> T {
        self.state.get()
    }

    pub fn set(&self, val: T) {
        self.state.set(val);
    }
}

// ----------------------------------------------------------------------------
// 3. OBSERVABLE OBJECT & PUBLISHED (SwiftUI ObservableObject / ArkUI @Observed)
// ----------------------------------------------------------------------------

pub trait ObservableObject: Send + Sync {
    fn object_will_change(&self);
}

#[derive(Clone)]
pub struct Published<T> {
    val: Arc<RwLock<T>>,
    notifier: Option<Arc<dyn Fn() + Send + Sync>>,
}

impl<T: Clone> Published<T> {
    pub fn new(val: T) -> Self {
        Self {
            val: Arc::new(RwLock::new(val)),
            notifier: None,
        }
    }

    pub fn with_notifier(val: T, notifier: Arc<dyn Fn() + Send + Sync>) -> Self {
        Self {
            val: Arc::new(RwLock::new(val)),
            notifier: Some(notifier),
        }
    }

    pub fn get(&self) -> T {
        self.val.read().unwrap().clone()
    }

    pub fn set(&self, new_val: T) {
        {
            let mut w = self.val.write().unwrap();
            *w = new_val;
        }
        if let Some(ref n) = self.notifier {
            n();
        }
    }
}

// ----------------------------------------------------------------------------
// 4. ENVIRONMENT & APP STORAGE (SwiftUI @Environment / ArkUI @StorageLink)
// ----------------------------------------------------------------------------

#[derive(Default, Clone)]
pub struct EnvironmentValues {
    store: Arc<RwLock<HashMap<TypeId, Box<dyn Any + Send + Sync>>>>,
}

impl EnvironmentValues {
    pub fn new() -> Self {
        Self {
            store: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    pub fn insert<T: 'static + Send + Sync>(&self, val: T) {
        let mut lock = self.store.write().unwrap();
        lock.insert(TypeId::of::<T>(), Box::new(val));
    }

    pub fn get<T: 'static + Clone + Send + Sync>(&self) -> Option<T> {
        let lock = self.store.read().unwrap();
        lock.get(&TypeId::of::<T>())
            .and_then(|boxed| boxed.downcast_ref::<T>())
            .cloned()
    }
}
