"""
Module providing Growth Cone class for growth cone representation.
"""
import math

from simulation.growth_cone.history import History


class GrowthCone:
    """
    Represents a growth cone in the simulation environment.

    Attributes:
        pos_start (tuple): Initial position of the growth cone.
        pos_current (tuple): Center point of the circular modeled growth cone (x, y coordinates).
        pos_new (tuple): Potential new position for the growth cone (used for step decision).
        size (int): Radius of the growth cone.
        ligand_current (float): Ligand value associated with the growth cone.
        receptor_current (float): Receptor value associated with the growth cone.
        potential (int): Current potential of the growth cone.

    Methods:
        __str__(): Provides a string representation of the growth cone instance.
    """

    def __init__(self, position, size, ligand, receptor, id):
        """
        Initializes a GrowthCone object with position, size, ligand, and receptor values.

        :param position: Initial position of the growth cone (x, y coordinates).
        :param size: Radius of the circular modeled growth cone.
        :param ligand: Ligand value associated with the growth cone.
        :param receptor: Receptor value associated with the growth cone.
        """
        self.pos_start = position
        self.pos_current = position
        self.pos_new = position

        self.size = size

        self.ligand_start = ligand
        self.receptor_start = receptor
        self.ligand_current = ligand
        self.receptor_current = receptor

        self.potential = 0
        self.adap_co = 1  # Adaptation coefficient starts at 1
        self.reset_force_receptor = 0  # Resetting forces start at 0
        self.reset_force_ligand = 0
        self.id = id

        self.history = History(self.potential, self.adap_co, self.pos_current, self.ligand_start, self.receptor_start,
                               self.reset_force_receptor, self.reset_force_ligand)

    def __str__(self):
        """
        Provides a string representation of the growth cone's attributes.
        """
        return (f"Receptor: {self.receptor_current}, Ligand: {self.ligand_current}, Position: {self.pos_current}, "
                f"Start Position: {self.pos_start}, Potential: {self.potential}, "
                f"ID: {self.id}, Adaptation Coefficient: {self.adap_co}, "
                f"Reset Forces: {self.reset_force_ligand}, {self.reset_force_receptor}")

    def take_step(self, new_potential):
        self.history.update_potential(new_potential)
        self.history.update_position(self.pos_new)
        self.potential = new_potential
        self.pos_current = self.pos_new

    def calculate_adaptation(self, mu, lambda_, h):
        """
        Calculate the adaptation coefficient and the resetting force based on the history.

        :param mu: Adjusting parameter for the adaptation coefficient.
        :param lambda_: Adjusting parameter for the resetting force.
        :param h: The number of historical steps to consider for adaptation.
        """
        # Ensure we have enough history to calculate adaptation
        if len(self.history.potential) >= h:
            recent_history = self.history.potential[-h:]  # Get the last h elements from the history

            # Calculate the adaptation coefficient using the formula from the paper
            adap_co_temp = 1 + math.log(
                1 + mu * sum(k * abs(potential_diff) for k, potential_diff in enumerate(recent_history, 1)) / sum(
                    range(1, h + 1)))

            self.adap_co = float("{:.6f}".format(adap_co_temp))

            # Calculate the resetting force
            self.reset_force_receptor = lambda_ * (self.receptor_start - self.receptor_current)
            self.reset_force_ligand = lambda_ * (self.ligand_start - self.ligand_current)

        self.history.update_adap_co(self.adap_co)
        self.history.update_reset_force_receptor(self.reset_force_receptor)
        self.history.update_reset_force_ligand(self.reset_force_ligand)

    def apply_adaptation(self):
        """
        Apply the adaptation coefficient and resetting force to the ligand and receptor values.
        """
        ligand_temp = self.ligand_current * self.adap_co
        receptor_temp = self.receptor_current * self.adap_co
        ligand_temp = max(0, ligand_temp + self.reset_force_ligand)
        receptor_temp = max(0, receptor_temp + self.reset_force_receptor)

        self.ligand_current = float("{:.6f}".format(ligand_temp))
        self.receptor_current = float("{:.6f}".format(receptor_temp))

        self.history.update_ligand(self.ligand_current)
        self.history.update_receptor(self.receptor_current)

    def apply_knock_in_with_receptor(self, receptor_increase):
        self.receptor_current += receptor_increase
        # self.ligand_current = 0.33 / self.receptor_current
