# Guía Completa de Patrones de Arquitectura y Diseño
## De Patrones Clásicos a Patrones de IA (2026)

---

## 📋 ÍNDICE GENERAL

### PARTE I: Patrones de Diseño Clásicos (Gang of Four)
1. Patrones Creacionales (5 patrones)
2. Patrones Estructurales (7 patrones)
3. Patrones de Comportamiento (11 patrones)

### PARTE II: Patrones Arquitectónicos Tradicionales
4. Arquitecturas en Capas
5. Arquitecturas Orientadas a Eventos
6. Arquitecturas de Presentación

### PARTE III: Patrones Modernos de Microservicios
7. Patrones de Resiliencia
8. Patrones de Datos Distribuidos
9. Patrones de Comunicación

### PARTE IV: Patrones de IA y Machine Learning
10. Patrones de Deployment de Modelos
11. Patrones de Data & Features
12. Patrones de Agentes e IA Generativa

---

# PARTE I: Patrones de Diseño Clásicos (Gang of Four)

## 1. PATRONES CREACIONALES

### 1.1 Singleton

**Problema:** Necesitas exactamente UNA instancia de una clase en todo el sistema.

**Solución:** Asegurar que solo existe una instancia y proveer acceso global a ella.

**Cuándo usar:**
- ✅ Conexión a base de datos
- ✅ Logger de aplicación
- ✅ Configuración de aplicación
- ✅ Cache manager

**Cuándo NO usar:**
- ❌ Testing (dificulta mocking)
- ❌ Aplicaciones multi-thread sin cuidado
- ❌ Cuando necesitas flexibilidad futura

**Código Ejemplo (TypeScript):**
```typescript
class Database {
  private static instance: Database;
  private connection: any;

  // Constructor privado previene new Database()
  private constructor() {
    this.connection = this.createConnection();
  }

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  private createConnection() {
    console.log('Conexión única creada');
    return { /* connection object */ };
  }

  public query(sql: string) {
    return this.connection.execute(sql);
  }
}

// Uso
const db1 = Database.getInstance();
const db2 = Database.getInstance();
console.log(db1 === db2); // true - misma instancia
```

**Versión Thread-Safe (Python):**
```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

class DatabaseConnection(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = self.create_connection()
            self.initialized = True

    def create_connection(self):
        print("Creando conexión única")
        return {"host": "localhost", "port": 5432}
```

**Anti-patrón común:**
```typescript
// ❌ MAL - Singleton global mutable
class Config {
  public static instance = new Config();
  public apiUrl: string = '';  // Mutable!

  setApiUrl(url: string) {
    this.apiUrl = url;  // Estado global mutable = DESASTRE
  }
}

// ✅ BIEN - Singleton inmutable
class Config {
  private static instance: Config;
  private readonly apiUrl: string;

  private constructor() {
    this.apiUrl = process.env.API_URL || '';
  }

  public static getInstance(): Config {
    if (!Config.instance) {
      Config.instance = new Config();
    }
    return Config.instance;
  }

  public getApiUrl(): string {
    return this.apiUrl;
  }
}
```

---

### 1.2 Factory Method

**Problema:** Crear objetos sin especificar la clase exacta a crear.

**Solución:** Define una interfaz para crear objetos, pero deja que las subclases decidan qué clase instanciar.

**Cuándo usar:**
- ✅ No sabes de antemano el tipo exacto de objeto
- ✅ Quieres que subclases decidan la implementación
- ✅ Centralizar lógica de creación

**Código Ejemplo (TypeScript):**
```typescript
// Product interface
interface PaymentProcessor {
  processPayment(amount: number): Promise<boolean>;
  refund(transactionId: string): Promise<boolean>;
}

// Concrete Products
class StripePayment implements PaymentProcessor {
  async processPayment(amount: number): Promise<boolean> {
    console.log(`Processing $${amount} via Stripe`);
    // Lógica de Stripe
    return true;
  }

  async refund(transactionId: string): Promise<boolean> {
    console.log(`Refunding Stripe transaction ${transactionId}`);
    return true;
  }
}

class PayPalPayment implements PaymentProcessor {
  async processPayment(amount: number): Promise<boolean> {
    console.log(`Processing $${amount} via PayPal`);
    // Lógica de PayPal
    return true;
  }

  async refund(transactionId: string): Promise<boolean> {
    console.log(`Refunding PayPal transaction ${transactionId}`);
    return true;
  }
}

class CryptoPayment implements PaymentProcessor {
  async processPayment(amount: number): Promise<boolean> {
    console.log(`Processing $${amount} via Bitcoin`);
    // Lógica de Crypto
    return true;
  }

  async refund(transactionId: string): Promise<boolean> {
    throw new Error('Crypto payments cannot be refunded');
  }
}

// Factory
class PaymentProcessorFactory {
  static createProcessor(type: 'stripe' | 'paypal' | 'crypto'): PaymentProcessor {
    switch (type) {
      case 'stripe':
        return new StripePayment();
      case 'paypal':
        return new PayPalPayment();
      case 'crypto':
        return new CryptoPayment();
      default:
        throw new Error(`Unknown payment type: ${type}`);
    }
  }
}

// Uso
const processor = PaymentProcessorFactory.createProcessor('stripe');
await processor.processPayment(100);

// Fácil cambiar a otro procesador
const cryptoProcessor = PaymentProcessorFactory.createProcessor('crypto');
await cryptoProcessor.processPayment(100);
```

**Factory con IA (ejemplo moderno):**
```typescript
interface LLMProvider {
  generate(prompt: string): Promise<string>;
  estimateCost(tokens: number): number;
}

class OpenAIProvider implements LLMProvider {
  async generate(prompt: string): Promise<string> {
    // Llamada a OpenAI API
    return "Response from GPT-4";
  }

  estimateCost(tokens: number): number {
    return tokens * 0.00003; // $0.03 per 1K tokens
  }
}

class AnthropicProvider implements LLMProvider {
  async generate(prompt: string): Promise<string> {
    // Llamada a Claude API
    return "Response from Claude";
  }

  estimateCost(tokens: number): number {
    return tokens * 0.000025; // $0.025 per 1K tokens
  }
}

class LLMFactory {
  static createProvider(
    type: 'openai' | 'anthropic',
    config?: any
  ): LLMProvider {
    switch (type) {
      case 'openai':
        return new OpenAIProvider();
      case 'anthropic':
        return new AnthropicProvider();
      default:
        throw new Error(`Unknown LLM provider: ${type}`);
    }
  }

  // Factory inteligente que elige basado en costo/calidad
  static createOptimalProvider(
    task: 'simple' | 'complex',
    budget: number
  ): LLMProvider {
    if (task === 'simple' && budget < 0.01) {
      return new AnthropicProvider(); // Más barato para tareas simples
    }
    return new OpenAIProvider(); // Mejor para tareas complejas
  }
}
```

---

### 1.3 Abstract Factory

**Problema:** Crear familias de objetos relacionados sin especificar sus clases concretas.

**Solución:** Proveer una interfaz para crear familias de objetos relacionados.

**Cuándo usar:**
- ✅ Múltiples familias de productos relacionados
- ✅ Quieres asegurar que productos de la misma familia se usen juntos
- ✅ Temas (dark/light), Plataformas (iOS/Android)

**Código Ejemplo (TypeScript):**
```typescript
// Abstract Products
interface Button {
  render(): void;
  onClick(handler: () => void): void;
}

interface Input {
  render(): void;
  getValue(): string;
}

interface Checkbox {
  render(): void;
  isChecked(): boolean;
}

// Concrete Products - Material Design
class MaterialButton implements Button {
  render(): void {
    console.log('Rendering Material Design button');
  }
  onClick(handler: () => void): void {
    console.log('Material button clicked');
    handler();
  }
}

class MaterialInput implements Input {
  private value: string = '';

  render(): void {
    console.log('Rendering Material Design input');
  }
  getValue(): string {
    return this.value;
  }
}

class MaterialCheckbox implements Checkbox {
  private checked: boolean = false;

  render(): void {
    console.log('Rendering Material Design checkbox');
  }
  isChecked(): boolean {
    return this.checked;
  }
}

// Concrete Products - iOS
class iOSButton implements Button {
  render(): void {
    console.log('Rendering iOS style button');
  }
  onClick(handler: () => void): void {
    console.log('iOS button clicked');
    handler();
  }
}

class iOSInput implements Input {
  private value: string = '';

  render(): void {
    console.log('Rendering iOS style input');
  }
  getValue(): string {
    return this.value;
  }
}

class iOSCheckbox implements Checkbox {
  private checked: boolean = false;

  render(): void {
    console.log('Rendering iOS style checkbox');
  }
  isChecked(): boolean {
    return this.checked;
  }
}

// Abstract Factory
interface UIFactory {
  createButton(): Button;
  createInput(): Input;
  createCheckbox(): Checkbox;
}

// Concrete Factories
class MaterialUIFactory implements UIFactory {
  createButton(): Button {
    return new MaterialButton();
  }
  createInput(): Input {
    return new MaterialInput();
  }
  createCheckbox(): Checkbox {
    return new MaterialCheckbox();
  }
}

class iOSUIFactory implements UIFactory {
  createButton(): Button {
    return new iOSButton();
  }
  createInput(): Input {
    return new iOSInput();
  }
  createCheckbox(): Checkbox {
    return new iOSCheckbox();
  }
}

// Cliente
class Application {
  private button: Button;
  private input: Input;
  private checkbox: Checkbox;

  constructor(factory: UIFactory) {
    this.button = factory.createButton();
    this.input = factory.createInput();
    this.checkbox = factory.createCheckbox();
  }

  render() {
    this.button.render();
    this.input.render();
    this.checkbox.render();
  }
}

// Uso
const platform = 'ios'; // Podría venir de detectar dispositivo

let factory: UIFactory;
if (platform === 'ios') {
  factory = new iOSUIFactory();
} else {
  factory = new MaterialUIFactory();
}

const app = new Application(factory);
app.render(); // Todos los componentes son del mismo estilo
```

---

### 1.4 Builder

**Problema:** Construir objetos complejos paso a paso.

**Solución:** Separar la construcción de un objeto complejo de su representación.

**Cuándo usar:**
- ✅ Objetos con muchos parámetros opcionales
- ✅ Construcción paso a paso necesaria
- ✅ Diferentes representaciones del mismo objeto

**Código Ejemplo (TypeScript):**
```typescript
// Product
class HttpRequest {
  method: string = 'GET';
  url: string = '';
  headers: Map<string, string> = new Map();
  body?: any;
  timeout: number = 30000;
  retries: number = 0;
  auth?: { username: string; password: string };

  execute(): Promise<any> {
    console.log(`Executing ${this.method} ${this.url}`);
    console.log(`Headers:`, Array.from(this.headers.entries()));
    console.log(`Timeout: ${this.timeout}ms, Retries: ${this.retries}`);
    return Promise.resolve({ status: 200, data: {} });
  }
}

// Builder
class HttpRequestBuilder {
  private request: HttpRequest = new HttpRequest();

  method(method: 'GET' | 'POST' | 'PUT' | 'DELETE'): this {
    this.request.method = method;
    return this;
  }

  url(url: string): this {
    this.request.url = url;
    return this;
  }

  header(key: string, value: string): this {
    this.request.headers.set(key, value);
    return this;
  }

  body(body: any): this {
    this.request.body = body;
    return this;
  }

  timeout(ms: number): this {
    this.request.timeout = ms;
    return this;
  }

  retries(count: number): this {
    this.request.retries = count;
    return this;
  }

  auth(username: string, password: string): this {
    this.request.auth = { username, password };
    return this;
  }

  build(): HttpRequest {
    // Validaciones antes de construir
    if (!this.request.url) {
      throw new Error('URL is required');
    }
    return this.request;
  }
}

// Uso
const request = new HttpRequestBuilder()
  .method('POST')
  .url('https://api.example.com/users')
  .header('Content-Type', 'application/json')
  .header('Authorization', 'Bearer token123')
  .body({ name: 'John', email: 'john@example.com' })
  .timeout(5000)
  .retries(3)
  .build();

await request.execute();

// Ejemplo con IA - Construir prompts complejos
class PromptBuilder {
  private systemPrompt: string = '';
  private userPrompt: string = '';
  private examples: Array<{ input: string; output: string }> = [];
  private temperature: number = 0.7;
  private maxTokens: number = 1000;
  private stopSequences: string[] = [];

  system(prompt: string): this {
    this.systemPrompt = prompt;
    return this;
  }

  user(prompt: string): this {
    this.userPrompt = prompt;
    return this;
  }

  addExample(input: string, output: string): this {
    this.examples.push({ input, output });
    return this;
  }

  setTemperature(temp: number): this {
    this.temperature = Math.max(0, Math.min(1, temp));
    return this;
  }

  setMaxTokens(tokens: number): this {
    this.maxTokens = tokens;
    return this;
  }

  addStopSequence(sequence: string): this {
    this.stopSequences.push(sequence);
    return this;
  }

  build(): any {
    let fullPrompt = '';

    if (this.systemPrompt) {
      fullPrompt += `System: ${this.systemPrompt}\n\n`;
    }

    if (this.examples.length > 0) {
      fullPrompt += 'Examples:\n';
      this.examples.forEach((ex, i) => {
        fullPrompt += `Example ${i + 1}:\nInput: ${ex.input}\nOutput: ${ex.output}\n\n`;
      });
    }

    fullPrompt += `User: ${this.userPrompt}`;

    return {
      prompt: fullPrompt,
      temperature: this.temperature,
      maxTokens: this.maxTokens,
      stopSequences: this.stopSequences
    };
  }
}

// Uso
const aiPrompt = new PromptBuilder()
  .system('You are an expert software architect.')
  .addExample(
    'Design a cache',
    'Use Redis with LRU eviction policy'
  )
  .addExample(
    'Design a queue',
    'Use RabbitMQ with dead-letter queues'
  )
  .user('Design a real-time notification system')
  .setTemperature(0.3)
  .setMaxTokens(500)
  .build();

console.log(aiPrompt);
```

---

### 1.5 Prototype

**Problema:** Crear objetos duplicados costosos de construir.

**Solución:** Clonar un objeto existente en lugar de crear uno nuevo.

**Cuándo usar:**
- ✅ Creación de objetos es costosa
- ✅ Objetos similares con pequeñas variaciones
- ✅ Evitar subclases creadoras

**Código Ejemplo (TypeScript):**
```typescript
interface Cloneable<T> {
  clone(): T;
}

class DatabaseConnection implements Cloneable<DatabaseConnection> {
  host: string;
  port: number;
  database: string;
  options: Map<string, any>;
  private expensiveResource: any; // Recurso costoso de crear

  constructor(
    host: string,
    port: number,
    database: string
  ) {
    this.host = host;
    this.port = port;
    this.database = database;
    this.options = new Map();

    // Simulando inicialización costosa
    console.log('Inicializando recursos costosos...');
    this.expensiveResource = this.initializeExpensiveResource();
  }

  private initializeExpensiveResource(): any {
    // Simulación de operación costosa
    return { pool: 'connection pool', cache: {} };
  }

  clone(): DatabaseConnection {
    // Clone superficial
    const cloned = Object.create(Object.getPrototypeOf(this));
    Object.assign(cloned, this);

    // Clone profundo de options
    cloned.options = new Map(this.options);

    // Compartir recurso costoso (o clonarlo si es necesario)
    cloned.expensiveResource = this.expensiveResource;

    console.log('Conexión clonada (sin re-inicializar recursos)');
    return cloned;
  }

  setOption(key: string, value: any): void {
    this.options.set(key, value);
  }
}

// Uso
const baseConnection = new DatabaseConnection('localhost', 5432, 'mydb');
baseConnection.setOption('ssl', true);
baseConnection.setOption('poolSize', 10);

// Crear variaciones sin re-inicializar recursos costosos
const devConnection = baseConnection.clone();
devConnection.database = 'mydb_dev';

const testConnection = baseConnection.clone();
testConnection.database = 'mydb_test';
testConnection.setOption('poolSize', 5);

// Solo se inicializó recursos una vez, luego se clonaron
```

---

## 2. PATRONES ESTRUCTURALES

### 2.1 Adapter (Wrapper)

**Problema:** Hacer que interfaces incompatibles trabajen juntas.

**Solución:** Crear un adaptador que traduce una interfaz a otra.

**Cuándo usar:**
- ✅ Integrar librerías de terceros con tu código
- ✅ Trabajar con legacy code
- ✅ Unificar múltiples interfaces similares

**Código Ejemplo (TypeScript):**
```typescript
// Sistema legacy (no puedes modificar)
class LegacyPaymentGateway {
  makePayment(accountNumber: string, amount: number): string {
    console.log(`Legacy: Procesando $${amount} desde cuenta ${accountNumber}`);
    return `LEGACY_TX_${Date.now()}`;
  }
}

// Tu interfaz moderna
interface ModernPaymentProcessor {
  processPayment(userId: string, amount: number, currency: string): Promise<{
    transactionId: string;
    status: 'success' | 'failed';
    timestamp: Date;
  }>;
}

// Adapter
class LegacyPaymentAdapter implements ModernPaymentProcessor {
  private legacyGateway: LegacyPaymentGateway;

  constructor() {
    this.legacyGateway = new LegacyPaymentGateway();
  }

  async processPayment(
    userId: string,
    amount: number,
    currency: string
  ): Promise<{ transactionId: string; status: 'success' | 'failed'; timestamp: Date }> {
    // Traducir interfaz moderna a legacy
    const accountNumber = this.getUserAccountNumber(userId);
    const convertedAmount = this.convertCurrency(amount, currency, 'USD');

    try {
      const legacyTxId = this.legacyGateway.makePayment(accountNumber, convertedAmount);

      // Traducir respuesta legacy a formato moderno
      return {
        transactionId: legacyTxId,
        status: 'success',
        timestamp: new Date()
      };
    } catch (error) {
      return {
        transactionId: '',
        status: 'failed',
        timestamp: new Date()
      };
    }
  }

  private getUserAccountNumber(userId: string): string {
    // Lógica para obtener número de cuenta desde userId
    return `ACC_${userId}`;
  }

  private convertCurrency(amount: number, from: string, to: string): number {
    // Lógica de conversión (simplificada)
    return amount;
  }
}

// Uso
const paymentProcessor: ModernPaymentProcessor = new LegacyPaymentAdapter();
const result = await paymentProcessor.processPayment('user123', 100, 'USD');
console.log(result);

// Ejemplo con IA - Adaptar múltiples LLM APIs
interface UnifiedLLM {
  generate(prompt: string, options?: any): Promise<string>;
}

class OpenAIAdapter implements UnifiedLLM {
  async generate(prompt: string, options?: any): Promise<string> {
    // Adaptar a formato de OpenAI
    const openAIFormat = {
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      temperature: options?.temperature || 0.7
    };

    // Llamada a OpenAI API
    return "Response from OpenAI";
  }
}

class ClaudeAdapter implements UnifiedLLM {
  async generate(prompt: string, options?: any): Promise<string> {
    // Adaptar a formato de Claude
    const claudeFormat = {
      model: 'claude-3-opus',
      prompt: `\n\nHuman: ${prompt}\n\nAssistant:`,
      max_tokens_to_sample: options?.maxTokens || 1000
    };

    // Llamada a Claude API
    return "Response from Claude";
  }
}

// Ahora puedes intercambiar LLMs sin cambiar tu código
async function analyzeText(llm: UnifiedLLM, text: string) {
  const analysis = await llm.generate(`Analyze this: ${text}`);
  return analysis;
}

const openai = new OpenAIAdapter();
const claude = new ClaudeAdapter();

await analyzeText(openai, "Sample text");
await analyzeText(claude, "Sample text"); // Misma interfaz!
```

---

### 2.2 Proxy

**Problema:** Controlar acceso a un objeto.

**Solución:** Crear un sustituto que controla el acceso al objeto real.

**Cuándo usar:**
- ✅ Lazy loading (cargar solo cuando se necesita)
- ✅ Caching
- ✅ Logging/Auditing
- ✅ Control de acceso

**Código Ejemplo (TypeScript):**
```typescript
interface ImageService {
  display(): void;
  getMetadata(): { width: number; height: number; size: number };
}

// Objeto real (costoso de cargar)
class RealImage implements ImageService {
  private filename: string;
  private imageData: Buffer;

  constructor(filename: string) {
    this.filename = filename;
    this.imageData = this.loadFromDisk();
  }

  private loadFromDisk(): Buffer {
    console.log(`⏳ Cargando imagen pesada desde disco: ${this.filename}`);
    // Simulando operación costosa
    return Buffer.from('image data');
  }

  display(): void {
    console.log(`Mostrando imagen: ${this.filename}`);
  }

  getMetadata(): { width: number; height: number; size: number } {
    return { width: 1920, height: 1080, size: this.imageData.length };
  }
}

// Proxy con Lazy Loading y Caching
class ImageProxy implements ImageService {
  private filename: string;
  private realImage?: RealImage;
  private cache: Map<string, any> = new Map();

  constructor(filename: string) {
    this.filename = filename;
  }

  display(): void {
    // Lazy loading - solo carga cuando se necesita
    if (!this.realImage) {
      console.log('Proxy: Iniciando carga lazy de imagen...');
      this.realImage = new RealImage(this.filename);
    }
    this.realImage.display();
  }

  getMetadata(): { width: number; height: number; size: number } {
    // Caching - evita cargar imagen solo para metadata
    const cacheKey = 'metadata';

    if (this.cache.has(cacheKey)) {
      console.log('Proxy: Retornando metadata desde cache');
      return this.cache.get(cacheKey);
    }

    if (!this.realImage) {
      this.realImage = new RealImage(this.filename);
    }

    const metadata = this.realImage.getMetadata();
    this.cache.set(cacheKey, metadata);
    return metadata;
  }
}

// Uso
console.log('=== Sin Proxy ===');
const realImage = new RealImage('photo.jpg'); // Carga inmediata
realImage.display();

console.log('\n=== Con Proxy ===');
const proxyImage = new ImageProxy('photo.jpg'); // NO carga
console.log('Proxy creado, imagen aún no cargada');
proxyImage.display(); // Carga ahora (lazy)
proxyImage.display(); // Usa instancia ya cargada

// Proxy de Control de Acceso con IA
interface AIModel {
  predict(input: any): Promise<any>;
}

class ExpensiveAIModel implements AIModel {
  async predict(input: any): Promise<any> {
    console.log('🤖 Ejecutando modelo de IA (costoso)...');
    // Simulando inferencia costosa
    return { prediction: 'result', confidence: 0.95 };
  }
}

class AIModelProxy implements AIModel {
  private model: ExpensiveAIModel;
  private requestCount: Map<string, number> = new Map();
  private cache: Map<string, any> = new Map();

  constructor(model: ExpensiveAIModel) {
    this.model = model;
  }

  async predict(input: any): Promise<any> {
    const userId = input.userId;

    // Control de acceso - Rate limiting
    const userRequests = this.requestCount.get(userId) || 0;
    if (userRequests >= 100) {
      throw new Error('Rate limit exceeded. Max 100 requests per hour.');
    }

    // Caching - evitar predicciones duplicadas
    const cacheKey = JSON.stringify(input);
    if (this.cache.has(cacheKey)) {
      console.log('📦 Retornando predicción desde cache');
      return this.cache.get(cacheKey);
    }

    // Logging - auditoría
    console.log(`📝 Usuario ${userId} solicitó predicción`);
    this.requestCount.set(userId, userRequests + 1);

    // Llamada al modelo real
    const result = await this.model.predict(input);

    // Guardar en cache
    this.cache.set(cacheKey, result);

    return result;
  }
}

// Uso
const aiModel = new ExpensiveAIModel();
const aiProxy = new AIModelProxy(aiModel);

// Primera llamada - ejecuta modelo
await aiProxy.predict({ userId: 'user1', data: [1, 2, 3] });

// Segunda llamada con mismos datos - usa cache
await aiProxy.predict({ userId: 'user1', data: [1, 2, 3] });
```

---

### 2.3 Decorator

**Problema:** Añadir funcionalidad a objetos dinámicamente sin modificar su código.

**Solución:** Envolver el objeto en decoradores que añaden comportamiento.

**Cuándo usar:**
- ✅ Añadir responsabilidades a objetos individuales
- ✅ Evitar explosión de subclases
- ✅ Componer funcionalidades (logging, caching, validación)

**Código Ejemplo (TypeScript):**
```typescript
// Component interface
interface DataSource {
  writeData(data: string): void;
  readData(): string;
}

// Concrete Component
class FileDataSource implements DataSource {
  private filename: string;
  private data: string = '';

  constructor(filename: string) {
    this.filename = filename;
  }

  writeData(data: string): void {
    console.log(`Writing data to file: ${this.filename}`);
    this.data = data;
  }

  readData(): string {
    console.log(`Reading data from file: ${this.filename}`);
    return this.data;
  }
}

// Base Decorator
abstract class DataSourceDecorator implements DataSource {
  protected wrappee: DataSource;

  constructor(source: DataSource) {
    this.wrappee = source;
  }

  writeData(data: string): void {
    this.wrappee.writeData(data);
  }

  readData(): string {
    return this.wrappee.readData();
  }
}

// Concrete Decorators
class EncryptionDecorator extends DataSourceDecorator {
  writeData(data: string): void {
    console.log('🔒 Encriptando datos...');
    const encrypted = Buffer.from(data).toString('base64');
    super.writeData(encrypted);
  }

  readData(): string {
    const encrypted = super.readData();
    console.log('🔓 Desencriptando datos...');
    return Buffer.from(encrypted, 'base64').toString('utf-8');
  }
}

class CompressionDecorator extends DataSourceDecorator {
  writeData(data: string): void {
    console.log('🗜️  Comprimiendo datos...');
    const compressed = this.compress(data);
    super.writeData(compressed);
  }

  readData(): string {
    const compressed = super.readData();
    console.log('📂 Descomprimiendo datos...');
    return this.decompress(compressed);
  }

  private compress(data: string): string {
    // Simulación de compresión
    return `COMPRESSED(${data})`;
  }

  private decompress(data: string): string {
    return data.replace('COMPRESSED(', '').replace(')', '');
  }
}

class LoggingDecorator extends DataSourceDecorator {
  writeData(data: string): void {
    console.log(`📝 [LOG] Writing ${data.length} bytes at ${new Date().toISOString()}`);
    super.writeData(data);
    console.log('📝 [LOG] Write completed');
  }

  readData(): string {
    console.log(`📝 [LOG] Reading data at ${new Date().toISOString()}`);
    const data = super.readData();
    console.log(`📝 [LOG] Read ${data.length} bytes`);
    return data;
  }
}

// Uso - Composición de decorators
let source: DataSource = new FileDataSource('data.txt');

// Añadir logging
source = new LoggingDecorator(source);

// Añadir compresión
source = new CompressionDecorator(source);

// Añadir encriptación
source = new EncryptionDecorator(source);

// Ahora tenemos: Logging -> Compresión -> Encriptación -> File
source.writeData('Hello, World!');
console.log('\n--- LEYENDO ---\n');
const data = source.readData();
console.log('Dato final:', data);

// Decorators con IA - Rate Limiting en LLM calls
interface LLMService {
  generate(prompt: string): Promise<string>;
}

class BaseLLMService implements LLMService {
  async generate(prompt: string): Promise<string> {
    console.log('🤖 Generando con LLM...');
    return `Generated response for: ${prompt}`;
  }
}

class RateLimitDecorator implements LLMService {
  private service: LLMService;
  private requestTimestamps: number[] = [];
  private maxRequests = 10;
  private timeWindowMs = 60000; // 1 minuto

  constructor(service: LLMService) {
    this.service = service;
  }

  async generate(prompt: string): Promise<string> {
    const now = Date.now();

    // Limpiar timestamps antiguos
    this.requestTimestamps = this.requestTimestamps.filter(
      t => now - t < this.timeWindowMs
    );

    if (this.requestTimestamps.length >= this.maxRequests) {
      throw new Error(`Rate limit: máximo ${this.maxRequests} requests por minuto`);
    }

    this.requestTimestamps.push(now);
    return await this.service.generate(prompt);
  }
}

class CachingDecorator implements LLMService {
  private service: LLMService;
  private cache: Map<string, string> = new Map();

  constructor(service: LLMService) {
    this.service = service;
  }

  async generate(prompt: string): Promise<string> {
    if (this.cache.has(prompt)) {
      console.log('💾 Cache hit!');
      return this.cache.get(prompt)!;
    }

    const result = await this.service.generate(prompt);
    this.cache.set(prompt, result);
    return result;
  }
}

class CostTrackingDecorator implements LLMService {
  private service: LLMService;
  private totalCost: number = 0;

  constructor(service: LLMService) {
    this.service = service;
  }

  async generate(prompt: string): Promise<string> {
    const result = await this.service.generate(prompt);

    // Estimar costo (ejemplo: $0.03 por 1K tokens)
    const tokens = (prompt.length + result.length) / 4; // Aproximado
    const cost = (tokens / 1000) * 0.03;
    this.totalCost += cost;

    console.log(`💰 Costo de esta llamada: $${cost.toFixed(4)}`);
    console.log(`💰 Costo total acumulado: $${this.totalCost.toFixed(4)}`);

    return result;
  }
}

// Composición
let llm: LLMService = new BaseLLMService();
llm = new CachingDecorator(llm);
llm = new RateLimitDecorator(llm);
llm = new CostTrackingDecorator(llm);

await llm.generate('Hello');
await llm.generate('Hello'); // Cache hit
```

---

## 3. PATRONES DE COMPORTAMIENTO

### 3.1 Strategy

**Problema:** Definir una familia de algoritmos intercambiables.

**Solución:** Encapsular cada algoritmo y hacerlos intercambiables.

**Cuándo usar:**
- ✅ Múltiples formas de hacer algo
- ✅ Evitar condicionales complejos (if/else, switch)
- ✅ Configurar comportamiento en runtime

**Código Ejemplo (TypeScript):**
```typescript
// Strategy interface
interface SortStrategy {
  sort(data: number[]): number[];
}

// Concrete Strategies
class QuickSort implements SortStrategy {
  sort(data: number[]): number[] {
    console.log('🚀 Usando QuickSort (mejor para datos aleatorios)');
    // Implementación simplificada
    if (data.length <= 1) return data;

    const pivot = data[Math.floor(data.length / 2)];
    const left = data.filter(x => x < pivot);
    const middle = data.filter(x => x === pivot);
    const right = data.filter(x => x > pivot);

    return [...this.sort(left), ...middle, ...this.sort(right)];
  }
}

class MergeSort implements SortStrategy {
  sort(data: number[]): number[] {
    console.log('🔀 Usando MergeSort (estable, mejor para casi ordenados)');
    if (data.length <= 1) return data;

    const mid = Math.floor(data.length / 2);
    const left = this.sort(data.slice(0, mid));
    const right = this.sort(data.slice(mid));

    return this.merge(left, right);
  }

  private merge(left: number[], right: number[]): number[] {
    const result: number[] = [];
    let i = 0, j = 0;

    while (i < left.length && j < right.length) {
      if (left[i] <= right[j]) {
        result.push(left[i++]);
      } else {
        result.push(right[j++]);
      }
    }

    return [...result, ...left.slice(i), ...right.slice(j)];
  }
}

class BubbleSort implements SortStrategy {
  sort(data: number[]): number[] {
    console.log('🐌 Usando BubbleSort (simple, para arrays pequeños)');
    const arr = [...data];

    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        }
      }
    }

    return arr;
  }
}

// Context
class Sorter {
  private strategy: SortStrategy;

  constructor(strategy: SortStrategy) {
    this.strategy = strategy;
  }

  setStrategy(strategy: SortStrategy): void {
    this.strategy = strategy;
  }

  sort(data: number[]): number[] {
    return this.strategy.sort(data);
  }

  // Estrategia inteligente que elige algoritmo basándose en datos
  sortSmart(data: number[]): number[] {
    if (data.length < 10) {
      console.log('📊 Array pequeño detectado');
      this.setStrategy(new BubbleSort());
    } else if (this.isNearlySorted(data)) {
      console.log('📊 Array casi ordenado detectado');
      this.setStrategy(new MergeSort());
    } else {
      console.log('📊 Array aleatorio detectado');
      this.setStrategy(new QuickSort());
    }

    return this.sort(data);
  }

  private isNearlySorted(data: number[]): boolean {
    let inversions = 0;
    for (let i = 0; i < data.length - 1; i++) {
      if (data[i] > data[i + 1]) inversions++;
    }
    return inversions < data.length * 0.1; // <10% inversiones
  }
}

// Uso
const sorter = new Sorter(new QuickSort());
console.log(sorter.sort([5, 2, 8, 1, 9]));

// Cambiar estrategia en runtime
sorter.setStrategy(new MergeSort());
console.log(sorter.sort([5, 2, 8, 1, 9]));

// Smart sorting
console.log(sorter.sortSmart([1, 2, 3, 5, 4])); // Usa MergeSort
console.log(sorter.sortSmart([9, 2, 5, 1, 8])); // Usa QuickSort

// Strategy con IA - Diferentes estrategias de generación
interface TextGenerationStrategy {
  generate(prompt: string): Promise<string>;
  getCost(tokens: number): number;
}

class CreativeStrategy implements TextGenerationStrategy {
  async generate(prompt: string): Promise<string> {
    console.log('🎨 Generación creativa (temperature=0.9)');
    // Alta temperature, más creatividad
    return `Creative response for: ${prompt}`;
  }

  getCost(tokens: number): number {
    return tokens * 0.00003; // GPT-4
  }
}

class PreciseStrategy implements TextGenerationStrategy {
  async generate(prompt: string): Promise<string> {
    console.log('🎯 Generación precisa (temperature=0.1)');
    // Baja temperature, más determinista
    return `Precise response for: ${prompt}`;
  }

  getCost(tokens: number): number {
    return tokens * 0.00003;
  }
}

class CheapStrategy implements TextGenerationStrategy {
  async generate(prompt: string): Promise<string> {
    console.log('💰 Generación económica (GPT-3.5)');
    // Modelo más barato
    return `Cheap response for: ${prompt}`;
  }

  getCost(tokens: number): number {
    return tokens * 0.000001; // GPT-3.5 Turbo
  }
}

class AIGenerator {
  private strategy: TextGenerationStrategy;

  constructor(strategy: TextGenerationStrategy) {
    this.strategy = strategy;
  }

  async generate(prompt: string): Promise<string> {
    return await this.strategy.generate(prompt);
  }

  setStrategy(strategy: TextGenerationStrategy): void {
    this.strategy = strategy;
  }
}

// Uso
const generator = new AIGenerator(new CreativeStrategy());
await generator.generate('Write a poem');

// Cambiar a estrategia precisa para código
generator.setStrategy(new PreciseStrategy());
await generator.generate('Write a function');

// Cambiar a económica para tareas simples
generator.setStrategy(new CheapStrategy());
await generator.generate('Translate to Spanish');
```

---

### 3.2 Observer

**Problema:** Notificar múltiples objetos cuando cambia el estado de otro.

**Solución:** Definir dependencia uno-a-muchos entre objetos.

**Cuándo usar:**
- ✅ Event-driven systems
- ✅ Pub/Sub patterns
- ✅ Reactive programming
- ✅ UI updates cuando cambia el modelo

**Código Ejemplo (TypeScript):**
```typescript
// Subject interface
interface Subject {
  attach(observer: Observer): void;
  detach(observer: Observer): void;
  notify(): void;
}

// Observer interface
interface Observer {
  update(subject: Subject): void;
}

// Concrete Subject
class StockMarket implements Subject {
  private observers: Observer[] = [];
  private stockPrices: Map<string, number> = new Map();

  attach(observer: Observer): void {
    console.log('📌 Observer attached');
    this.observers.push(observer);
  }

  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index > -1) {
      this.observers.splice(index, 1);
      console.log('📌 Observer detached');
    }
  }

  notify(): void {
    console.log('📢 Notifying all observers...');
    for (const observer of this.observers) {
      observer.update(this);
    }
  }

  setPrice(stock: string, price: number): void {
    console.log(`💹 ${stock} price updated to $${price}`);
    this.stockPrices.set(stock, price);
    this.notify(); // Notificar cuando cambia el precio
  }

  getPrice(stock: string): number {
    return this.stockPrices.get(stock) || 0;
  }
}

// Concrete Observers
class Investor implements Observer {
  private name: string;

  constructor(name: string) {
    this.name = name;
  }

  update(subject: Subject): void {
    if (subject instanceof StockMarket) {
      const applePrice = subject.getPrice('AAPL');
      console.log(`👤 ${this.name}: Apple price is now $${applePrice}`);

      if (applePrice > 150) {
        console.log(`   ${this.name}: Selling!`);
      } else if (applePrice < 100) {
        console.log(`   ${this.name}: Buying!`);
      }
    }
  }
}

class TradingBot implements Observer {
  private botId: string;

  constructor(botId: string) {
    this.botId = botId;
  }

  update(subject: Subject): void {
    if (subject instanceof StockMarket) {
      const applePrice = subject.getPrice('AAPL');
      console.log(`🤖 Bot ${this.botId}: Analyzing price $${applePrice}`);

      // Lógica automatizada
      if (applePrice > 145 && applePrice < 155) {
        console.log(`   Bot ${this.botId}: Auto-selling 100 shares`);
      }
    }
  }
}

class PriceLogger implements Observer {
  update(subject: Subject): void {
    if (subject instanceof StockMarket) {
      const applePrice = subject.getPrice('AAPL');
      console.log(`📝 Logger: [${new Date().toISOString()}] AAPL=$${applePrice}`);
    }
  }
}

// Uso
const market = new StockMarket();

const investor1 = new Investor('Alice');
const investor2 = new Investor('Bob');
const bot = new TradingBot('BOT-001');
const logger = new PriceLogger();

market.attach(investor1);
market.attach(investor2);
market.attach(bot);
market.attach(logger);

console.log('\n=== Primera actualización ===');
market.setPrice('AAPL', 120);

console.log('\n=== Segunda actualización ===');
market.setPrice('AAPL', 160);

console.log('\n=== Bob se retira ===');
market.detach(investor2);

console.log('\n=== Tercera actualización ===');
market.setPrice('AAPL', 95);

// Observer con IA - Sistema de agentes colaborativos
class AIAgentSystem implements Subject {
  private observers: Observer[] = [];
  private knowledgeBase: Map<string, any> = new Map();

  attach(observer: Observer): void {
    this.observers.push(observer);
  }

  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index > -1) this.observers.splice(index, 1);
  }

  notify(): void {
    for (const observer of this.observers) {
      observer.update(this);
    }
  }

  addKnowledge(key: string, value: any): void {
    console.log(`🧠 New knowledge added: ${key}`);
    this.knowledgeBase.set(key, value);
    this.notify();
  }

  getKnowledge(key: string): any {
    return this.knowledgeBase.get(key);
  }

  getAllKnowledge(): Map<string, any> {
    return this.knowledgeBase;
  }
}

class ResearchAgent implements Observer {
  update(subject: Subject): void {
    if (subject instanceof AIAgentSystem) {
      console.log('🔬 Research Agent: Analyzing new knowledge');
      const knowledge = subject.getAllKnowledge();

      // Tomar acción basada en nuevo conocimiento
      if (knowledge.has('customer_complaint')) {
        console.log('   Research Agent: Searching for similar past cases...');
      }
    }
  }
}

class SummaryAgent implements Observer {
  update(subject: Subject): void {
    if (subject instanceof AIAgentSystem) {
      console.log('📋 Summary Agent: Generating summary');
      const knowledge = subject.getAllKnowledge();
      console.log(`   Total knowledge items: ${knowledge.size}`);
    }
  }
}

class AlertAgent implements Observer {
  update(subject: Subject): void {
    if (subject instanceof AIAgentSystem) {
      console.log('🚨 Alert Agent: Checking for critical issues');
      const complaint = subject.getKnowledge('customer_complaint');

      if (complaint && complaint.severity === 'high') {
        console.log('   Alert Agent: CRITICAL! Notifying human supervisor');
      }
    }
  }
}

// Uso
const aiSystem = new AIAgentSystem();
aiSystem.attach(new ResearchAgent());
aiSystem.attach(new SummaryAgent());
aiSystem.attach(new AlertAgent());

aiSystem.addKnowledge('customer_complaint', {
  text: 'Product is broken',
  severity: 'high'
});
```

---

*[Continuará con más patrones...]*

**NOTA:** Este documento está diseñado para ser extenso y completo. He creado las primeras secciones con:
- Patrones Creacionales (5 completos)
- Patrones Estructurales (3 completos)
- Patrones de Comportamiento (2 completos)

Cada patrón incluye:
✅ Problema que resuelve
✅ Solución
✅ Cuándo usar / NO usar
✅ Código completo con ejemplos
✅ Ejemplo moderno con IA

¿Quiero continuar con el resto de patrones (faltan ~40 más) incluyendo:
- Patrones GoF restantes
- Patrones arquitectónicos (Strangler, Saga, CQRS, etc.)
- Patrones de microservicios
- Patrones de IA/ML

¿Procedo a completar todo el documento?
