# Conocimientos Técnicos Difíciles: Mobile Development

## Objetivo
Temas complejos específicos del desarrollo móvil (iOS, Android, React Native, Flutter) que un arquitecto debe dominar para apoyar efectivamente a desarrolladores mobile.

---

## CATEGORÍA 1: Native Performance Optimization

### 1.1 iOS Performance (Swift/Objective-C)
**Dificultad:** ⭐⭐⭐⭐⭐

**Instruments Profiling:**

```swift
// 1. Memory Management - ARC (Automatic Reference Counting)

// ❌ Retain Cycle (Memory Leak)
class ViewController: UIViewController {
    var closure: (() -> Void)?

    func setupClosure() {
        closure = {
            // PROBLEM: self retained by closure, closure retained by self
            self.view.backgroundColor = .red
        }
    }
}

// ✅ Weak reference para evitar retain cycle
class ViewController: UIViewController {
    var closure: (() -> Void)?

    func setupClosure() {
        closure = { [weak self] in
            guard let self = self else { return }
            self.view.backgroundColor = .red
        }
    }
}

// 2. UITableView/UICollectionView optimization
class OptimizedTableViewController: UITableViewController {

    // ✅ Cell reuse
    override func tableView(_ tableView: UITableView,
                           cellForRowAt indexPath: IndexPath) -> UITableViewCell {

        // Reuse cells en lugar de crear nuevas
        let cell = tableView.dequeueReusableCell(
            withIdentifier: "CellIdentifier",
            for: indexPath
        ) as! CustomCell

        // Configure cell
        let item = items[indexPath.row]
        cell.configure(with: item)

        return cell
    }

    // ✅ Height caching
    private var heightCache: [IndexPath: CGFloat] = [:]

    override func tableView(_ tableView: UITableView,
                           estimatedHeightForRowAt indexPath: IndexPath) -> CGFloat {
        return heightCache[indexPath] ?? 100
    }

    override func tableView(_ tableView: UITableView,
                           willDisplay cell: UITableViewCell,
                           forRowAt indexPath: IndexPath) {
        // Cache actual height
        heightCache[indexPath] = cell.frame.height
    }
}

// 3. Image loading y caching
class ImageLoader {
    static let shared = ImageLoader()

    private let cache = NSCache<NSString, UIImage>()
    private let downloadQueue = DispatchQueue(
        label: "com.app.imageloader",
        qos: .userInitiated,
        attributes: .concurrent
    )

    func loadImage(from url: URL, completion: @escaping (UIImage?) -> Void) {
        let key = url.absoluteString as NSString

        // Check cache
        if let cachedImage = cache.object(forKey: key) {
            completion(cachedImage)
            return
        }

        // Download
        downloadQueue.async {
            guard let data = try? Data(contentsOf: url),
                  let image = UIImage(data: data) else {
                completion(nil)
                return
            }

            // Cache image
            self.cache.setObject(image, forKey: key)

            // Return on main thread
            DispatchQueue.main.async {
                completion(image)
            }
        }
    }

    // Image downsampling para memory efficiency
    func downsampleImage(at url: URL, to targetSize: CGSize) -> UIImage? {
        let imageSourceOptions = [kCGImageSourceShouldCache: false] as CFDictionary

        guard let imageSource = CGImageSourceCreateWithURL(
            url as CFURL,
            imageSourceOptions
        ) else {
            return nil
        }

        let maxDimensionInPixels = max(targetSize.width, targetSize.height) *
                                   UIScreen.main.scale

        let downsampleOptions = [
            kCGImageSourceCreateThumbnailFromImageAlways: true,
            kCGImageSourceShouldCacheImmediately: true,
            kCGImageSourceCreateThumbnailWithTransform: true,
            kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels
        ] as CFDictionary

        guard let downsampledImage = CGImageSourceCreateThumbnailAtIndex(
            imageSource,
            0,
            downsampleOptions
        ) else {
            return nil
        }

        return UIImage(cgImage: downsampledImage)
    }
}

// 4. Background processing
class DataSyncManager {

    func syncDataInBackground() {
        // Background task para continuar después de app en background
        var backgroundTask: UIBackgroundTaskIdentifier = .invalid

        backgroundTask = UIApplication.shared.beginBackgroundTask {
            // Cleanup cuando expira el tiempo
            UIApplication.shared.endBackgroundTask(backgroundTask)
            backgroundTask = .invalid
        }

        DispatchQueue.global(qos: .background).async {
            // Sync logic
            self.performSync()

            // End task
            UIApplication.shared.endBackgroundTask(backgroundTask)
            backgroundTask = .invalid
        }
    }

    private func performSync() {
        // Heavy sync operation
    }
}

// 5. Core Data performance
class CoreDataManager {
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "Model")

        container.loadPersistentStores { (description, error) in
            if let error = error {
                fatalError("Core Data store failed: \(error)")
            }
        }

        // Performance optimizations
        container.viewContext.automaticallyMergesChangesFromParent = true
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy

        return container
    }()

    // Background context para operaciones pesadas
    func performBackgroundTask(_ block: @escaping (NSManagedObjectContext) -> Void) {
        persistentContainer.performBackgroundTask { context in
            // Set batch size para queries grandes
            context.stalenessInterval = 0

            block(context)

            // Save si hay cambios
            if context.hasChanges {
                do {
                    try context.save()
                } catch {
                    print("Background save failed: \(error)")
                }
            }
        }
    }

    // Batch operations
    func batchDeleteOldRecords() {
        let fetchRequest = NSFetchRequest<NSFetchRequestResult>(entityName: "Record")
        fetchRequest.predicate = NSPredicate(
            format: "createdAt < %@",
            Calendar.current.date(byAdding: .day, value: -30, to: Date())! as CVarArg
        )

        let batchDelete = NSBatchDeleteRequest(fetchRequest: fetchRequest)
        batchDelete.resultType = .resultTypeObjectIDs

        performBackgroundTask { context in
            do {
                let result = try context.execute(batchDelete) as? NSBatchDeleteResult
                let objectIDArray = result?.result as? [NSManagedObjectID]

                // Merge changes to main context
                let changes = [NSDeletedObjectsKey: objectIDArray ?? []]
                NSManagedObjectContext.mergeChanges(
                    fromRemoteContextSave: changes,
                    into: [self.persistentContainer.viewContext]
                )
            } catch {
                print("Batch delete failed: \(error)")
            }
        }
    }
}

// 6. SwiftUI Performance
struct OptimizedListView: View {
    @State private var items: [Item] = []

    var body: some View {
        List {
            // ✅ Use LazyVStack for better performance
            LazyVStack {
                ForEach(items) { item in
                    ItemRow(item: item)
                        .id(item.id) // Stable identity
                }
            }
        }
        .onAppear {
            loadItems()
        }
    }

    private func loadItems() {
        Task {
            // Load asynchronously
            items = await fetchItems()
        }
    }
}

// Evitar re-renders innecesarios
struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            // Cache rendered views
            Text(item.title)
                .font(.headline)

            Spacer()

            Text(item.subtitle)
                .font(.subheadline)
                .foregroundColor(.gray)
        }
        .padding()
    }
}

// Use @StateObject for view models
class ItemViewModel: ObservableObject {
    @Published var items: [Item] = []

    func loadItems() async {
        items = await fetchItems()
    }
}

struct ContentView: View {
    // ✅ StateObject for ownership
    @StateObject private var viewModel = ItemViewModel()

    var body: some View {
        List(viewModel.items) { item in
            Text(item.title)
        }
        .task {
            await viewModel.loadItems()
        }
    }
}
```

---

### 1.2 Android Performance (Kotlin)
**Dificultad:** ⭐⭐⭐⭐⭐

```kotlin
// 1. RecyclerView Optimization
class OptimizedAdapter : RecyclerView.Adapter<OptimizedAdapter.ViewHolder>() {

    private val items = mutableListOf<Item>()

    // ViewHolder pattern
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        private val titleView: TextView = view.findViewById(R.id.title)
        private val imageView: ImageView = view.findViewById(R.id.image)

        fun bind(item: Item) {
            titleView.text = item.title

            // Load image with Glide (caching automático)
            Glide.with(itemView.context)
                .load(item.imageUrl)
                .placeholder(R.drawable.placeholder)
                .into(imageView)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_layout, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun getItemCount() = items.size

    // DiffUtil para updates eficientes
    fun updateItems(newItems: List<Item>) {
        val diffCallback = ItemDiffCallback(items, newItems)
        val diffResult = DiffUtil.calculateDiff(diffCallback)

        items.clear()
        items.addAll(newItems)
        diffResult.dispatchUpdatesTo(this)
    }
}

class ItemDiffCallback(
    private val oldList: List<Item>,
    private val newList: List<Item>
) : DiffUtil.Callback() {

    override fun getOldListSize() = oldList.size
    override fun getNewListSize() = newList.size

    override fun areItemsTheSame(oldItemPosition: Int, newItemPosition: Int): Boolean {
        return oldList[oldItemPosition].id == newList[newItemPosition].id
    }

    override fun areContentsTheSame(oldItemPosition: Int, newItemPosition: Int): Boolean {
        return oldList[oldItemPosition] == newList[newItemPosition]
    }
}

// 2. Coroutines para operaciones async
class DataRepository(
    private val api: ApiService,
    private val database: AppDatabase
) {
    // Dispatcher apropiado para cada operación
    suspend fun fetchData(): Result<List<Item>> = withContext(Dispatchers.IO) {
        try {
            val response = api.getItems()

            if (response.isSuccessful) {
                response.body()?.let { items ->
                    // Cache en database
                    database.itemDao().insertAll(items)
                    Result.success(items)
                } ?: Result.failure(Exception("Empty response"))
            } else {
                Result.failure(Exception("API error: ${response.code()}"))
            }
        } catch (e: Exception) {
            // Fallback a cached data
            val cachedItems = database.itemDao().getAll()
            if (cachedItems.isNotEmpty()) {
                Result.success(cachedItems)
            } else {
                Result.failure(e)
            }
        }
    }

    // Flow para reactive updates
    fun observeItems(): Flow<List<Item>> = database.itemDao().observeAll()
        .flowOn(Dispatchers.IO)
}

// 3. ViewModel con StateFlow
class ItemViewModel(
    private val repository: DataRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    init {
        loadItems()
    }

    fun loadItems() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading

            repository.fetchData()
                .onSuccess { items ->
                    _uiState.value = UiState.Success(items)
                }
                .onFailure { error ->
                    _uiState.value = UiState.Error(error.message ?: "Unknown error")
                }
        }
    }

    // Observe database changes
    fun observeItems() {
        viewModelScope.launch {
            repository.observeItems()
                .collect { items ->
                    _uiState.value = UiState.Success(items)
                }
        }
    }
}

sealed class UiState {
    object Loading : UiState()
    data class Success(val items: List<Item>) : UiState()
    data class Error(val message: String) : UiState()
}

// 4. Jetpack Compose Performance
@Composable
fun OptimizedListScreen(viewModel: ItemViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    when (uiState) {
        is UiState.Loading -> LoadingIndicator()
        is UiState.Success -> {
            val items = (uiState as UiState.Success).items

            // LazyColumn for efficient scrolling
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp)
            ) {
                items(
                    items = items,
                    key = { item -> item.id } // Stable keys
                ) { item ->
                    ItemCard(
                        item = item,
                        modifier = Modifier.animateItemPlacement() // Smooth animations
                    )
                }
            }
        }
        is UiState.Error -> ErrorView((uiState as UiState.Error).message)
    }
}

@Composable
fun ItemCard(item: Item, modifier: Modifier = Modifier) {
    // remember para evitar recreación
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        elevation = 4.dp
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // AsyncImage con caching
            AsyncImage(
                model = ImageRequest.Builder(LocalContext.current)
                    .data(item.imageUrl)
                    .crossfade(true)
                    .build(),
                contentDescription = null,
                modifier = Modifier.size(64.dp)
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column {
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.h6
                )
                Text(
                    text = item.subtitle,
                    style = MaterialTheme.typography.body2,
                    color = Color.Gray
                )
            }
        }
    }
}

// 5. Room Database optimization
@Database(entities = [Item::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun itemDao(): ItemDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                    // Migrations
                    .addMigrations(MIGRATION_1_2)
                    // Multi-threaded support
                    .setJournalMode(RoomDatabase.JournalMode.WRITE_AHEAD_LOGGING)
                    .build()

                INSTANCE = instance
                instance
            }
        }
    }
}

@Dao
interface ItemDao {
    @Query("SELECT * FROM items ORDER BY createdAt DESC")
    fun observeAll(): Flow<List<Item>>

    @Query("SELECT * FROM items WHERE id = :id")
    suspend fun getById(id: String): Item?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<Item>)

    @Query("DELETE FROM items WHERE createdAt < :timestamp")
    suspend fun deleteOlderThan(timestamp: Long)

    // Paginación
    @Query("SELECT * FROM items ORDER BY createdAt DESC LIMIT :limit OFFSET :offset")
    suspend fun getPage(limit: Int, offset: Int): List<Item>
}

// 6. WorkManager para background tasks
class SyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        return try {
            val repository = DataRepository(/* inject dependencies */)

            repository.fetchData()
                .onSuccess {
                    Result.success()
                }
                .onFailure {
                    Result.retry()
                }

            Result.success()
        } catch (e: Exception) {
            Result.failure()
        }
    }
}

// Schedule periodic sync
class SyncScheduler(private val context: Context) {
    fun scheduleSync() {
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .setRequiresBatteryNotLow(true)
            .build()

        val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(
            15, TimeUnit.MINUTES // Minimum interval
        )
            .setConstraints(constraints)
            .setBackoffCriteria(
                BackoffPolicy.EXPONENTIAL,
                10, TimeUnit.SECONDS
            )
            .build()

        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            "data_sync",
            ExistingPeriodicWorkPolicy.KEEP,
            syncRequest
        )
    }
}
```

---

## CATEGORÍA 2: Cross-Platform Development

### 2.1 React Native Performance
**Dificultad:** ⭐⭐⭐⭐

```javascript
// 1. FlatList optimization
import React, { useCallback, useMemo } from 'react';
import { FlatList, View, Text } from 'react-native';

const OptimizedList = ({ data }) => {
  // Memoize render function
  const renderItem = useCallback(({ item }) => (
    <ItemComponent item={item} />
  ), []);

  // Key extractor
  const keyExtractor = useCallback((item) => item.id, []);

  // Get item layout para scroll performance
  const getItemLayout = useCallback(
    (data, index) => ({
      length: ITEM_HEIGHT,
      offset: ITEM_HEIGHT * index,
      index,
    }),
    []
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      getItemLayout={getItemLayout}
      // Performance props
      removeClippedSubviews={true}
      maxToRenderPerBatch={10}
      updateCellsBatchingPeriod={50}
      initialNumToRender={10}
      windowSize={5}
      // Pull to refresh
      onRefresh={onRefresh}
      refreshing={refreshing}
    />
  );
};

// 2. Memoization para evitar re-renders
const ItemComponent = React.memo(({ item }) => {
  return (
    <View style={styles.item}>
      <Text>{item.title}</Text>
      <Text>{item.description}</Text>
    </View>
  );
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.item.id === nextProps.item.id &&
         prevProps.item.title === nextProps.item.title;
});

// 3. Native modules para performance crítica
// NativeModules/ImageProcessor.ts (TypeScript)
import { NativeModules } from 'react-native';

interface ImageProcessorInterface {
  compressImage(
    path: string,
    quality: number
  ): Promise<string>;

  resizeImage(
    path: string,
    width: number,
    height: number
  ): Promise<string>;
}

const { ImageProcessor } = NativeModules;

export default ImageProcessor as ImageProcessorInterface;

// Implementación nativa (iOS - Swift)
@objc(ImageProcessor)
class ImageProcessor: NSObject {

  @objc
  func compressImage(_ path: String,
                    quality: NSNumber,
                    resolver: @escaping RCTPromiseResolveBlock,
                    rejecter: @escaping RCTPromiseRejectBlock) {

    DispatchQueue.global(qos: .userInitiated).async {
      guard let image = UIImage(contentsOfFile: path) else {
        rejecter("ERROR", "Failed to load image", nil)
        return
      }

      let qualityFloat = quality.floatValue
      guard let compressedData = image.jpegData(compressionQuality: CGFloat(qualityFloat)) else {
        rejecter("ERROR", "Failed to compress", nil)
        return
      }

      // Save compressed image
      let outputPath = NSTemporaryDirectory() + "compressed.jpg"
      try? compressedData.write(to: URL(fileURLWithPath: outputPath))

      resolver(outputPath)
    }
  }

  @objc
  static func requiresMainQueueSetup() -> Bool {
    return false
  }
}

// 4. Hermes engine optimization
// Enable Hermes in android/app/build.gradle
project.ext.react = [
    enableHermes: true
]

// 5. Reanimated para animations performantes
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming
} from 'react-native-reanimated';

const AnimatedComponent = () => {
  const offset = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => {
    return {
      transform: [{ translateX: offset.value }],
    };
  });

  const handlePress = () => {
    // Runs on UI thread!
    offset.value = withSpring(offset.value + 100);
  };

  return (
    <Animated.View style={animatedStyle}>
      <Pressable onPress={handlePress}>
        <Text>Animate</Text>
      </Pressable>
    </Animated.View>
  );
};

// 6. Code splitting y lazy loading
import React, { Suspense, lazy } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

const App = () => {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <HeavyComponent />
    </Suspense>
  );
};
```

---

### 2.2 Flutter Performance
**Dificultad:** ⭐⭐⭐⭐

```dart
// 1. ListView optimization
class OptimizedListView extends StatelessWidget {
  final List<Item> items;

  const OptimizedListView({Key? key, required this.items}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      // Only builds visible items
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        return ItemTile(key: ValueKey(item.id), item: item);
      },
      // Prevent rebuild when scrolling back
      addAutomaticKeepAlives: true,
      // Reuse elements
      addRepaintBoundaries: true,
    );
  }
}

// 2. Const constructors para performance
class ItemTile extends StatelessWidget {
  final Item item;

  const ItemTile({Key? key, required this.item}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.person), // const!
        title: Text(item.title),
        subtitle: Text(item.subtitle),
      ),
    );
  }
}

// 3. Riverpod para state management eficiente
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider
final itemsProvider = FutureProvider<List<Item>>((ref) async {
  final repository = ref.watch(repositoryProvider);
  return repository.fetchItems();
});

// Widget con consumer
class ItemListScreen extends ConsumerWidget {
  const ItemListScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final itemsAsync = ref.watch(itemsProvider);

    return itemsAsync.when(
      data: (items) => OptimizedListView(items: items),
      loading: () => const CircularProgressIndicator(),
      error: (error, stack) => ErrorWidget(error.toString()),
    );
  }
}

// 4. Compute para operaciones pesadas (isolates)
Future<List<Item>> parseItemsInBackground(String jsonString) async {
  return await compute(_parseItems, jsonString);
}

// Top-level function para isolate
List<Item> _parseItems(String jsonString) {
  final List<dynamic> jsonList = json.decode(jsonString);
  return jsonList.map((json) => Item.fromJson(json)).toList();
}

// 5. Cached network images
import 'package:cached_network_image/cached_network_image.dart';

class OptimizedImage extends StatelessWidget {
  final String imageUrl;

  const OptimizedImage({Key? key, required this.imageUrl}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: imageUrl,
      placeholder: (context, url) => const CircularProgressIndicator(),
      errorWidget: (context, url, error) => const Icon(Icons.error),
      // Memory cache
      memCacheWidth: 200,
      memCacheHeight: 200,
    );
  }
}

// 6. Drift (formerly Moor) para database
import 'package:drift/drift.dart';

@DataClassName('Item')
class Items extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get title => text()();
  TextColumn get subtitle => text()();
  DateTimeColumn get createdAt => dateTime()();
}

@DriftDatabase(tables: [Items])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  // Queries
  Future<List<Item>> getAllItems() => select(items).get();

  Stream<List<Item>> watchAllItems() => select(items).watch();

  Future insertItem(ItemsCompanion item) => into(items).insert(item);

  Future updateItem(Item item) => update(items).replace(item);

  Future deleteItem(Item item) => delete(items).delete(item);
}

// Open connection
LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'db.sqlite'));
    return NativeDatabase(file);
  });
}
```

---

## CATEGORÍA 3: Offline-First Architecture

### 3.1 Sync Strategies
**Dificultad:** ⭐⭐⭐⭐⭐

```kotlin
// 1. Offline-first repository pattern
class OfflineFirstRepository(
    private val localDataSource: LocalDataSource,
    private val remoteDataSource: RemoteDataSource,
    private val syncManager: SyncManager
) {

    // Read: Always from local, sync in background
    fun getItems(): Flow<Result<List<Item>>> = flow {
        // Emit cached data immediately
        val cachedItems = localDataSource.getItems()
        emit(Result.success(cachedItems))

        // Try to sync from server
        try {
            val remoteItems = remoteDataSource.fetchItems()

            // Update local cache
            localDataSource.saveItems(remoteItems)

            // Emit updated data
            emit(Result.success(remoteItems))
        } catch (e: Exception) {
            // If sync fails, keep cached data
            // User already has data from cache
        }
    }

    // Write: Save locally, queue for sync
    suspend fun createItem(item: Item): Result<Item> {
        // Generate temporary ID
        val localItem = item.copy(
            id = UUID.randomUUID().toString(),
            syncStatus = SyncStatus.PENDING
        )

        // Save to local database
        localDataSource.insertItem(localItem)

        // Queue for sync
        syncManager.queueForSync(
            SyncOperation.Create(localItem)
        )

        return Result.success(localItem)
    }

    suspend fun updateItem(item: Item): Result<Item> {
        val updatedItem = item.copy(
            syncStatus = SyncStatus.PENDING,
            updatedAt = System.currentTimeMillis()
        )

        localDataSource.updateItem(updatedItem)

        syncManager.queueForSync(
            SyncOperation.Update(updatedItem)
        )

        return Result.success(updatedItem)
    }
}

// 2. Sync Manager con conflict resolution
class SyncManager(
    private val localDataSource: LocalDataSource,
    private val remoteDataSource: RemoteDataSource,
    private val workManager: WorkManager
) {

    fun queueForSync(operation: SyncOperation) {
        // Save operation to queue
        val syncQueue = SyncQueueDatabase.getInstance()
        syncQueue.insertOperation(operation)

        // Schedule worker
        val workRequest = OneTimeWorkRequestBuilder<SyncWorker>()
            .setConstraints(
                Constraints.Builder()
                    .setRequiredNetworkType(NetworkType.CONNECTED)
                    .build()
            )
            .setBackoffCriteria(
                BackoffPolicy.EXPONENTIAL,
                10, TimeUnit.SECONDS
            )
            .build()

        workManager.enqueue(workRequest)
    }

    suspend fun performSync() {
        val operations = SyncQueueDatabase.getInstance()
            .getPendingOperations()

        for (operation in operations) {
            try {
                when (operation) {
                    is SyncOperation.Create -> syncCreate(operation)
                    is SyncOperation.Update -> syncUpdate(operation)
                    is SyncOperation.Delete -> syncDelete(operation)
                }

                // Mark as synced
                SyncQueueDatabase.getInstance()
                    .markAsSynced(operation.id)

            } catch (e: ConflictException) {
                // Handle conflict
                resolveConflict(operation, e.serverVersion)
            } catch (e: Exception) {
                // Retry later
                SyncQueueDatabase.getInstance()
                    .incrementRetryCount(operation.id)
            }
        }
    }

    private suspend fun syncCreate(operation: SyncOperation.Create) {
        val item = operation.item

        // Send to server
        val serverItem = remoteDataSource.createItem(item)

        // Update local with server ID
        localDataSource.updateItem(
            item.copy(
                id = serverItem.id,
                syncStatus = SyncStatus.SYNCED
            )
        )
    }

    private suspend fun syncUpdate(operation: SyncOperation.Update) {
        val item = operation.item

        try {
            // Send to server with version for optimistic locking
            remoteDataSource.updateItem(item, item.version)

            // Mark as synced
            localDataSource.updateItem(
                item.copy(syncStatus = SyncStatus.SYNCED)
            )

        } catch (e: VersionMismatchException) {
            // Conflict detected
            throw ConflictException(e.serverVersion)
        }
    }

    private suspend fun resolveConflict(
        operation: SyncOperation,
        serverVersion: Item
    ) {
        // Conflict resolution strategies:

        // 1. Server wins (default)
        localDataSource.updateItem(serverVersion)

        // 2. Client wins
        // remoteDataSource.forceUpdate(operation.item)

        // 3. Manual merge
        // presentConflictToUser(operation.item, serverVersion)

        // 4. Last write wins
        if (operation.item.updatedAt > serverVersion.updatedAt) {
            remoteDataSource.forceUpdate(operation.item)
        } else {
            localDataSource.updateItem(serverVersion)
        }
    }
}

sealed class SyncOperation {
    abstract val id: String

    data class Create(val item: Item) : SyncOperation() {
        override val id = item.id
    }

    data class Update(val item: Item) : SyncOperation() {
        override val id = item.id
    }

    data class Delete(val itemId: String) : SyncOperation() {
        override val id = itemId
    }
}

enum class SyncStatus {
    PENDING,
    SYNCED,
    CONFLICT,
    ERROR
}
```

---

## CATEGORÍA 4: Platform-Specific Features

### 4.1 Deep Linking & Universal Links
**Dificultad:** ⭐⭐⭐⭐

```swift
// iOS - Universal Links
// 1. Configure associated domains in Xcode
// 2. Host apple-app-site-association file

// AppDelegate.swift
func application(_ application: UIApplication,
                continue userActivity: NSUserActivity,
                restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {

    guard userActivity.activityType == NSUserActivityTypeBrowsingWeb,
          let url = userActivity.webpageURL else {
        return false
    }

    return handleUniversalLink(url: url)
}

func handleUniversalLink(url: URL) -> Bool {
    // Parse URL
    guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true) else {
        return false
    }

    // Route based on path
    switch components.path {
    case "/product":
        if let productId = components.queryItems?.first(where: { $0.name == "id" })?.value {
            navigateToProduct(id: productId)
            return true
        }

    case "/user":
        if let userId = components.queryItems?.first(where: { $0.name == "id" })?.value {
            navigateToUser(id: userId)
            return true
        }

    default:
        return false
    }

    return false
}
```

```kotlin
// Android - App Links
// AndroidManifest.xml
<activity android:name=".MainActivity">
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:scheme="https"
            android:host="example.com"
            android:pathPrefix="/product" />
    </intent-filter>
</activity>

// MainActivity.kt
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    // Handle incoming link
    handleIntent(intent)
}

override fun onNewIntent(intent: Intent?) {
    super.onNewIntent(intent)
    intent?.let { handleIntent(it) }
}

private fun handleIntent(intent: Intent) {
    val action = intent.action
    val data = intent.data

    if (Intent.ACTION_VIEW == action && data != null) {
        handleDeepLink(data)
    }
}

private fun handleDeepLink(uri: Uri) {
    when (uri.path) {
        "/product" -> {
            val productId = uri.getQueryParameter("id")
            productId?.let { navigateToProduct(it) }
        }

        "/user" -> {
            val userId = uri.getQueryParameter("id")
            userId?.let { navigateToUser(it) }
        }
    }
}
```

---

## Resumen Prioridades Mobile

| Tema | Dificultad | Criticidad | Frecuencia | Prioridad |
|------|------------|------------|------------|-----------|
| iOS Performance | 5 | 5 | 5 | **CRÍTICA** |
| Android Performance | 5 | 5 | 5 | **CRÍTICA** |
| React Native Optimization | 4 | 4 | 4 | **ALTA** |
| Flutter Performance | 4 | 4 | 4 | **ALTA** |
| Offline-First Architecture | 5 | 5 | 4 | **CRÍTICA** |
| Sync Strategies | 5 | 5 | 3 | **CRÍTICA** |
| Deep Linking | 4 | 3 | 3 | **MEDIA** |

**Total de temas:** 18+ subtemas específicos de mobile
