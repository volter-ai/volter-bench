import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Zap } from 'lucide-react';
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
  meta: {
    battle_ended: boolean;
  };
}

export function MainGameSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = data.entities.player_creature;
  const opponentCreature = data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      <HUD player={data.entities.player} opponent={data.entities.opponent} />
      <div className="flex-grow flex flex-col">
        <Battlefield playerCreature={playerCreature} opponentCreature={opponentCreature} />
        <UserInterface playerCreature={playerCreature} availableButtonSlugs={availableButtonSlugs} emitButtonClick={emitButtonClick} />
      </div>
    </div>
  );
}

function HUD({ player, opponent }: { player: Player; opponent: Player }) {
  return (
    <nav className="bg-gray-800 text-white p-2 flex justify-between items-center">
      <PlayerCard uid={player.uid} playerName={player.display_name} imageUrl="/path/to/player-image.jpg" />
      <h1 className="text-2xl font-bold">Creature Battle</h1>
      <PlayerCard uid={opponent.uid} playerName={opponent.display_name} imageUrl="/path/to/opponent-image.jpg" />
    </nav>
  );
}

function Battlefield({ playerCreature, opponentCreature }: { playerCreature: Creature; opponentCreature: Creature }) {
  return (
    <div className="flex-grow flex justify-between items-center p-4">
      <div className="flex flex-col items-center">
        <CreatureCard
          uid={playerCreature.uid}
          name={playerCreature.display_name}
          imageUrl="/path/to/player-creature.jpg"
          hp={playerCreature.stats.hp}
          maxHp={playerCreature.stats.max_hp}
        />
        <div className="mt-2 flex space-x-2">
          <Sword size={20} /> <span>{playerCreature.stats.attack}</span>
          <Shield size={20} /> <span>{playerCreature.stats.defense}</span>
          <Zap size={20} /> <span>{playerCreature.stats.speed}</span>
        </div>
      </div>
      <div className="flex flex-col items-center">
        <CreatureCard
          uid={opponentCreature.uid}
          name={opponentCreature.display_name}
          imageUrl="/path/to/opponent-creature.jpg"
          hp={opponentCreature.stats.hp}
          maxHp={opponentCreature.stats.max_hp}
        />
        <div className="mt-2 flex space-x-2">
          <Sword size={20} /> <span>{opponentCreature.stats.attack}</span>
          <Shield size={20} /> <span>{opponentCreature.stats.defense}</span>
          <Zap size={20} /> <span>{opponentCreature.stats.speed}</span>
        </div>
      </div>
    </div>
  );
}

function UserInterface({ playerCreature, availableButtonSlugs, emitButtonClick }: { playerCreature: Creature; availableButtonSlugs: string[]; emitButtonClick: (slug: string) => void }) {
  return (
    <div className="bg-white p-4 rounded-t-lg shadow-lg">
      <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
        {/* Text box content goes here */}
        <p>Battle log and game messages will appear here.</p>
      </div>
      <div className="grid grid-cols-2 gap-2">
        {playerCreature.collections.skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            stats={`Damage: ${skill.stats.base_damage}`}
            disabled={!availableButtonSlugs.includes(skill.uid)}
            onClick={() => emitButtonClick(skill.uid)}
          />
        ))}
      </div>
    </div>
  );
}
