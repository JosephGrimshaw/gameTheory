import statics as st
import torch.nn as nn
import torch.optim as optim
import torch
import optuna
from torch.utils.data import DataLoader

def train(model, l2=False, lambda_reg=0.01):
    model.to("cuda")
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.05045326047741923, momentum=0.9016387709386692, weight_decay=1.506207184326175e-05)

    epochs = 100
    train_losses = []
    test_losses = []
    best_loss = 100
    for epoch in range(epochs):
        temp_loss = 0
        model.train()
        for x, y in st.train_loader:
            x, y = x.to('cuda'), y.to('cuda')
            optimizer.zero_grad()
            yhat = model(x)
            loss = criterion(yhat, y)
            if l2:
                l2_norm = sum(p.pow(2).sum() for p in model.parameters())
                loss += lambda_reg * l2_norm
            loss.backward()
            temp_loss += loss.item()
            #torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
        temp_loss /= len(st.train_loader)
        train_losses.append(temp_loss)

        temp_loss_test = 0
        model.eval()
        with torch.no_grad():
            for x, y in st.test_loader:
                x, y = x.to('cuda'), y.to('cuda')
                yhat = model(x)
                loss = criterion(yhat, y)
                temp_loss_test += loss.item()
            temp_loss_test /= len(st.test_loader)
            test_losses.append(temp_loss_test)
            if temp_loss_test < best_loss:
                save(model)
                best_loss = temp_loss_test

        print(f"Epoch {epoch}: \nTrain Loss: {temp_loss} \nTest Loss: {temp_loss_test} \nBest Loss: {best_loss}")

def save(model):
    torch.save(model.state_dict(), 'hawkDoveAI.pt')

def optunaTrain(epochs, model, train_loader, test_loader, criterion, optimizer, device, l2=False, lambda_reg=0.01):
    test_loader_len = len(test_loader)
    model.train()
    for epoch in range(epochs):
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            yhat = model(x)
            loss = criterion(yhat, y)
            if l2:
                l2_norm = sum(p.pow(2).sum() for p in model.parameters())
                loss += lambda_reg * l2_norm
            loss.backward()
            optimizer.step()

    total_loss = 0
    with torch.no_grad():
        model.eval()
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            yhat = model(x)
            loss = criterion(yhat, y)
            total_loss += loss.item()
    print(total_loss)
    return total_loss/test_loader_len

def objective(trial):
    batch_size = trial.suggest_int('batch_size', 16, 64)
    lr = trial.suggest_loguniform('lr', 1e-5, 1e-1)
    momentum = trial.suggest_uniform('momentum', 0.8, 0.99)
    weight_decay = trial.suggest_loguniform('weight_decay', 1e-5, 1e-1)
    dropout = trial.suggest_uniform('dropout', 0, 0.5)
    nHLayers = trial.suggest_int('hidden_layers', 1, 6)
    hLayerNeurones = trial.suggest_int('hidden_layer_neurones', 4, 128)

    train_loader = DataLoader(st.train_data, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(st.test_data, batch_size=batch_size, shuffle=False)

    model = st.Model(nHLayers, hLayerNeurones, dropout)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay)
    cost = optunaTrain(10, model, train_loader, test_loader, criterion, optimizer, device)
    print("Cost: ", cost)
    return cost

def findBestHyperParams(n_trials):
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=n_trials)

    print("Best Hyperparams: ", study.best_params)
    print("Best Accuracy: ", study.best_value)
    with open("optimalHyperParams.txt", "x") as f:
        f.write("Best HyperParams: ", study.best_params, "\n\n", "Best Accuracy:", study.best_value)
    f.close()


model = st.Model(5, 120, 0.019294138089291524)
train(model)
save(model)


#findBestHyperParams(500)