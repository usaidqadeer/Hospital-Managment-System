import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class DoctorsScreen extends StatefulWidget {
  final String token;

  const DoctorsScreen({
    super.key,
    required this.token,
  });

  @override
  State<DoctorsScreen> createState() => _DoctorsScreenState();
}

class _DoctorsScreenState extends State<DoctorsScreen> {
  final String baseUrl =
      'https://hospital-managment-system-production.up.railway.app';

  final TextEditingController searchController = TextEditingController();

  bool isLoading = true;
  String errorMessage = '';
  List<dynamic> doctors = [];

  Map<String, String> get headers => {
        'Authorization': 'Bearer ${widget.token}',
        'Content-Type': 'application/json',
      };

  @override
  void initState() {
    super.initState();
    getDoctors();
  }

  Future<void> getDoctors() async {
    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    try {
      final response = await http.get(
        Uri.parse('$baseUrl/doctors/?page=1&limit=100'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        setState(() {
          doctors = jsonDecode(response.body) as List<dynamic>;
        });
      } else {
        final data = jsonDecode(response.body);
        setState(() {
          errorMessage =
              data['detail']?.toString() ?? 'Doctors load نہیں ہوئے';
        });
      }
    } catch (_) {
      setState(() {
        errorMessage = 'Server سے connection نہیں ہو سکا';
      });
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  Future<void> searchDoctors() async {
    final name = searchController.text.trim();

    if (name.isEmpty) {
      await getDoctors();
      return;
    }

    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    try {
      final uri = Uri.parse('$baseUrl/doctors/search').replace(
        queryParameters: {'name': name},
      );

      final response = await http.get(uri, headers: headers);

      if (response.statusCode == 200) {
        setState(() {
          doctors = jsonDecode(response.body) as List<dynamic>;
        });
      } else {
        final data = jsonDecode(response.body);
        setState(() {
          errorMessage = data['detail']?.toString() ?? 'Search failed';
        });
      }
    } catch (_) {
      setState(() {
        errorMessage = 'Server سے connection نہیں ہو سکا';
      });
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  Future<void> showDoctorForm({
    Map<String, dynamic>? doctor,
  }) async {
    final nameController = TextEditingController(
      text: doctor?['name']?.toString() ?? '',
    );
    final specializationController = TextEditingController(
      text: doctor?['specialization']?.toString() ?? '',
    );
    final phoneController = TextEditingController(
      text: doctor?['phone']?.toString() ?? '',
    );

    final isEditing = doctor != null;

    await showDialog(
      context: context,
      builder: (dialogContext) {
        bool isSaving = false;

        return StatefulBuilder(
          builder: (context, setDialogState) {
            Future<void> saveDoctor() async {
              final name = nameController.text.trim();
              final specialization = specializationController.text.trim();
              final phone = phoneController.text.trim();

              if (name.isEmpty ||
                  specialization.isEmpty ||
                  phone.isEmpty) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('تمام fields مکمل کریں'),
                  ),
                );
                return;
              }

              setDialogState(() {
                isSaving = true;
              });

              try {
                final url = isEditing
                    ? '$baseUrl/doctors/${doctor['id']}'
                    : '$baseUrl/doctors/';

                final body = jsonEncode({
                  'name': name,
                  'specialization': specialization,
                  'phone': phone,
                });

                final response = isEditing
                    ? await http.put(
                        Uri.parse(url),
                        headers: headers,
                        body: body,
                      )
                    : await http.post(
                        Uri.parse(url),
                        headers: headers,
                        body: body,
                      );

                if (!mounted) return;

                if (response.statusCode == 200 ||
                    response.statusCode == 201) {
                  Navigator.pop(dialogContext);

                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        isEditing
                            ? 'Doctor updated successfully'
                            : 'Doctor added successfully',
                      ),
                    ),
                  );

                  await getDoctors();
                } else {
                  final data = jsonDecode(response.body);

                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        data['detail']?.toString() ?? 'Operation failed',
                      ),
                    ),
                  );
                }
              } catch (_) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Server سے connection نہیں ہو سکا'),
                  ),
                );
              } finally {
                if (dialogContext.mounted) {
                  setDialogState(() {
                    isSaving = false;
                  });
                }
              }
            }

            return AlertDialog(
              title: Text(isEditing ? 'Edit Doctor' : 'Add Doctor'),
              content: SizedBox(
                width: 420,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    TextField(
                      controller: nameController,
                      decoration: const InputDecoration(
                        labelText: 'Doctor Name',
                        prefixIcon: Icon(Icons.person),
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 15),
                    TextField(
                      controller: specializationController,
                      decoration: const InputDecoration(
                        labelText: 'Specialization',
                        prefixIcon: Icon(Icons.medical_services),
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 15),
                    TextField(
                      controller: phoneController,
                      keyboardType: TextInputType.phone,
                      decoration: const InputDecoration(
                        labelText: 'Phone',
                        prefixIcon: Icon(Icons.phone),
                        border: OutlineInputBorder(),
                      ),
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: isSaving
                      ? null
                      : () {
                          Navigator.pop(dialogContext);
                        },
                  child: const Text('Cancel'),
                ),
                ElevatedButton(
                  onPressed: isSaving ? null : saveDoctor,
                  child: isSaving
                      ? const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(strokeWidth: 3),
                        )
                      : Text(isEditing ? 'Update' : 'Save'),
                ),
              ],
            );
          },
        );
      },
    );

    nameController.dispose();
    specializationController.dispose();
    phoneController.dispose();
  }

  Future<void> deleteDoctor(Map<String, dynamic> doctor) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (dialogContext) {
        return AlertDialog(
          title: const Text('Delete Doctor'),
          content: Text(
            'کیا آپ ${doctor['name']} کو delete کرنا چاہتے ہیں؟',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(dialogContext, false);
              },
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(dialogContext, true);
              },
              child: const Text('Delete'),
            ),
          ],
        );
      },
    );

    if (confirm != true) return;

    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/doctors/${doctor['id']}'),
        headers: headers,
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Doctor deleted successfully'),
          ),
        );
        await getDoctors();
      } else {
        final data = jsonDecode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              data['detail']?.toString() ?? 'Delete failed',
            ),
          ),
        );
      }
    } catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Server سے connection نہیں ہو سکا'),
        ),
      );
    }
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xffF4F7FB),
      appBar: AppBar(
        title: const Text('Doctors Management'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            tooltip: 'Refresh',
            onPressed: getDoctors,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          showDoctorForm();
        },
        icon: const Icon(Icons.add),
        label: const Text('Add Doctor'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(25),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: searchController,
                    onSubmitted: (_) => searchDoctors(),
                    decoration: InputDecoration(
                      hintText: 'Search doctor by name',
                      prefixIcon: const Icon(Icons.search),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                ElevatedButton(
                  onPressed: searchDoctors,
                  child: const Padding(
                    padding: EdgeInsets.symmetric(
                      vertical: 16,
                      horizontal: 10,
                    ),
                    child: Text('Search'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 25),
            Expanded(
              child: isLoading
                  ? const Center(
                      child: CircularProgressIndicator(),
                    )
                  : errorMessage.isNotEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(
                                Icons.error_outline,
                                size: 70,
                                color: Colors.red,
                              ),
                              const SizedBox(height: 15),
                              Text(errorMessage),
                              const SizedBox(height: 15),
                              ElevatedButton(
                                onPressed: getDoctors,
                                child: const Text('Try Again'),
                              ),
                            ],
                          ),
                        )
                      : doctors.isEmpty
                          ? const Center(
                              child: Text(
                                'No doctors found',
                                style: TextStyle(fontSize: 20),
                              ),
                            )
                          : ListView.separated(
                              itemCount: doctors.length,
                              separatorBuilder: (_, __) =>
                                  const SizedBox(height: 14),
                              itemBuilder: (context, index) {
                                final doctor =
                                    Map<String, dynamic>.from(doctors[index]);

                                return Card(
                                  elevation: 3,
                                  child: ListTile(
                                    contentPadding: const EdgeInsets.all(18),
                                    leading: CircleAvatar(
                                      radius: 28,
                                      backgroundColor: Colors.blue.shade50,
                                      child: const Icon(
                                        Icons.medical_services,
                                        color: Colors.blue,
                                      ),
                                    ),
                                    title: Text(
                                      doctor['name']?.toString() ?? '',
                                      style: const TextStyle(
                                        fontSize: 19,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    subtitle: Padding(
                                      padding: const EdgeInsets.only(top: 6),
                                      child: Text(
                                        '${doctor['specialization'] ?? ''}\n'
                                        '${doctor['phone'] ?? ''}',
                                      ),
                                    ),
                                    isThreeLine: true,
                                    trailing: Wrap(
                                      spacing: 5,
                                      children: [
                                        IconButton(
                                          tooltip: 'Edit',
                                          onPressed: () {
                                            showDoctorForm(doctor: doctor);
                                          },
                                          icon: const Icon(
                                            Icons.edit,
                                            color: Colors.blue,
                                          ),
                                        ),
                                        IconButton(
                                          tooltip: 'Delete',
                                          onPressed: () {
                                            deleteDoctor(doctor);
                                          },
                                          icon: const Icon(
                                            Icons.delete,
                                            color: Colors.red,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                );
                              },
                            ),
            ),
          ],
        ),
      ),
    );
  }
}
