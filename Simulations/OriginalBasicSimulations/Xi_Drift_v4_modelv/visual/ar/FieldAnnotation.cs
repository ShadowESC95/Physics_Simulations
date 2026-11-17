// visual/ar/FieldAnnotation.cs
public class HoloField : MonoBehaviour {
    void Update() {
        SpatialMeshRenderer.RenderQuantumState(
            GetComponent<XiFieldLoader>().currentState,
            hologramOpacity: 0.8f
        );
    }
}
