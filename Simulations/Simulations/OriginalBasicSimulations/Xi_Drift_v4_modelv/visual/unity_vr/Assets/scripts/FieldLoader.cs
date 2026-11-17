using UnityEngine;
using System.IO;

public class FieldLoader : MonoBehaviour {
    public string dataPath = "output/xi_field_log.npy";

    void Start() {
        double[,,] xi = NpyLoader.Load<double[,,]>(dataPath);
        GameObject fieldVolume = CreateVolume(xi);
        fieldVolume.AddComponent<XRGrabInteractable>();
    }
}
