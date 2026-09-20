package com.oubuilder

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

private enum class Section(val label: String) {
    CHAT("Chat"),
    IMPORT("Import"),
    DESIGN("Design"),
    IMAGE_FLOW("Image Flow"),
    PREVIEW("Preview"),
    BUILD("Build"),
    HISTORY("History"),
    SETTINGS("Settings")
}

data class ProjectState(
    val name: String = "Untitled Project",
    val files: List<String> = emptyList(),
    val screens: List<String> = emptyList(),
    val cloudProvider: String? = null
)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { OUTBuilderApp() }
    }
}

@Composable
private fun OUTBuilderApp() {
    var section by remember { mutableStateOf(Section.CHAT) }
    var project by remember { mutableStateOf(ProjectState()) }
    var command by remember { mutableStateOf("") }

    MaterialTheme {
        Row(Modifier.fillMaxSize()) {
            NavigationRail {
                Section.entries.forEach { item ->
                    NavigationRailItem(
                        selected = section == item,
                        onClick = { section = item },
                        icon = {},
                        label = { Text(item.label) }
                    )
                }
            }

            Column(Modifier.fillMaxSize().padding(20.dp)) {
                Text("OU The Builder", style = MaterialTheme.typography.headlineMedium)
                Text(
                    "Project: ${project.name}",
                    style = MaterialTheme.typography.bodyMedium
                )
                Spacer(Modifier.height(16.dp))

                when (section) {
                    Section.CHAT -> ChatScreen(
                        command = command,
                        onCommandChange = { command = it },
                        onExecute = {
                            if (command.isNotBlank()) {
                                project = project.copy(
                                    files = project.files + "AI command: $command"
                                )
                                command = ""
                            }
                        }
                    )
                    Section.IMPORT -> Placeholder("Import", "ZIP / RAR / files / Use This Folder / Git")
                    Section.DESIGN -> Placeholder("Design", "Shared project design state")
                    Section.IMAGE_FLOW -> Placeholder("Image Flow", "Project asset pipeline")
                    Section.PREVIEW -> Placeholder("Preview", "Interactive preview driven by ProjectState")
                    Section.BUILD -> BuildScreen()
                    Section.HISTORY -> HistoryScreen(project.files)
                    Section.SETTINGS -> SettingsScreen(project)
                }
            }
        }
    }
}

@Composable
private fun ChatScreen(
    command: String,
    onCommandChange: (String) -> Unit,
    onExecute: () -> Unit
) {
    Column(Modifier.fillMaxSize()) {
        Text("What do you want to build?", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(8.dp))
        Text("The chat layer will eventually dispatch real Builder actions against the shared Project Engine.")
        Spacer(Modifier.weight(1f))
        OutlinedTextField(
            value = command,
            onValueChange = onCommandChange,
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text("Create a calculator app…") }
        )
        Spacer(Modifier.height(8.dp))
        Row {
            Text("Agent: Auto")
            Spacer(Modifier.weight(1f))
            Button(onClick = onExecute) { Text("Run") }
        }
    }
}

@Composable
private fun BuildScreen() {
    Column {
        Text("Build", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(12.dp))
        Text("Target")
        Spacer(Modifier.height(6.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            AssistChip(onClick = {}, label = { Text("Android APK") })
            AssistChip(onClick = {}, label = { Text("Web App") })
            AssistChip(onClick = {}, label = { Text("Hybrid App") })
        }
        Spacer(Modifier.height(20.dp))
        Text("Build Console")
        Spacer(Modifier.height(8.dp))
        Text("No build has been executed yet.")
    }
}

@Composable
private fun HistoryScreen(events: List<String>) {
    Column {
        Text("History", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(12.dp))
        if (events.isEmpty()) {
            Text("No project changes yet.")
        } else {
            LazyColumn {
                items(events) { Text("• $it") }
            }
        }
    }
}

@Composable
private fun SettingsScreen(project: ProjectState) {
    Column {
        Text("Settings", style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(16.dp))
        Text("Cloud Storage", style = MaterialTheme.typography.titleLarge)
        Spacer(Modifier.height(8.dp))
        Text("Connected provider: ${project.cloudProvider ?: "None"}")
        Spacer(Modifier.height(12.dp))
        Button(onClick = {}) { Text("Connect Google Drive") }
        OutlinedButton(onClick = {}) { Text("Connect MobiDrive") }
        OutlinedButton(onClick = {}) { Text("Connect another provider") }
        Spacer(Modifier.height(20.dp))
        Text("Authentication will use provider authorization; passwords are not collected by OU The Builder.")
    }
}

@Composable
private fun Placeholder(title: String, description: String) {
    Column {
        Text(title, style = MaterialTheme.typography.headlineSmall)
        Spacer(Modifier.height(8.dp))
        Text(description)
        Spacer(Modifier.height(16.dp))
        Text("This foundation screen is intentionally wired to the shared navigation. The underlying engine is the next implementation layer.")
    }
}
