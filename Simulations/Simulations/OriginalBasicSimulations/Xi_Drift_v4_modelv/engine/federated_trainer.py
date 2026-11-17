from torch.nn.parallel import DistributedDataParallel as DDP

def federated_step(model, local_data, rank):
    # Wrap model for distributed training
    ddp_model = DDP(model, device_ids=[rank])
    
    # Local training
    opt = torch.optim.SGD(ddp_model.parameters(), lr=0.01)
    loss_fn = torch.nn.MSELoss()
    for _ in range(10):  # Local epochs
        loss = loss_fn(ddp_model(local_data), local_data)
        loss.backward()
        opt.step()
    
    # Aggregate gradients via MPI
    for param in ddp_model.parameters():
        comm.Allreduce(param.grad, param.grad, op=MPI.SUM)

