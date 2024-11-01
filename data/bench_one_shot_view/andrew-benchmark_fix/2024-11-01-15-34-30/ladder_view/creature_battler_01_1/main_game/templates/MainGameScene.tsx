import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    foe_creature: Creature;
  };
  collections: {
    player_skill_queue: Skill[];
  };
}

const fallbackSkills: Skill[] = [
  {
    uid: 'attack',
    display_name: 'Attack',
    description: 'A basic attack',
    stats: { damage: 1 }
  },
  {
    uid: 'defend',
    display_name: 'Defend',
    description: 'Defend against incoming attacks',
    stats: { damage: 0 }
  }
];

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;
  const playerSkills = props.data.collections.player_skill_queue && props.data.collections.player_skill_queue.length > 0
    ? props.data.collections.player_skill_queue
    : fallbackSkills;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8 py-4" style={{ maxHeight: '50vh' }}>
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-green-500" />
          <CreatureCard
            uid={playerCreature?.uid || "player-creature"}
            name={playerCreature?.display_name || "Unknown"}
            hp={playerCreature?.stats.hp || 0}
            className="mb-2"
          />
          <span className="text-sm font-semibold">Player</span>
        </div>
        <Swords className="w-12 h-12 text-red-500" />
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={foeCreature?.uid || "foe-creature"}
            name={foeCreature?.display_name || "Unknown"}
            hp={foeCreature?.stats.hp || 0}
            className="mb-2"
          />
          <span className="text-sm font-semibold">Opponent</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300" style={{ minHeight: '30vh' }}>
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerSkills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
