import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: {
    damage: number;
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
  };
  uid: string;
  display_name: string;
  description: string;
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
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, foe_creature } = props.data.entities;

  const getSkillByUid = (uid: string) => {
    return player_creature?.collections.skills.find(skill => skill.uid === uid);
  };

  const renderCreatureCard = (creature: Creature | undefined, isPlayer: boolean) => {
    if (!creature) return null;
    return (
      <CreatureCard
        uid={creature.uid}
        name={creature.display_name}
        imageUrl={`/creatures/${creature.uid}.png`}
        hp={creature.stats.hp}
        maxHp={creature.stats.max_hp}
        className={isPlayer ? "transform scale-x-[-1]" : ""}
      />
    );
  };

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Shield className="mr-2" />
          <span>Player</span>
        </div>
        <div className="flex items-center">
          <span>Opponent</span>
          <Swords className="ml-2" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {renderCreatureCard(player_creature, true)}
        {renderCreatureCard(foe_creature, false)}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3 overflow-y-auto">
        {player_creature && player_creature.collections.skills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((skillUid) => {
              const skill = getSkillByUid(skillUid);
              return skill ? (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  onClick={() => emitButtonClick(skillUid)}
                />
              ) : null;
            })}
          </div>
        ) : (
          <p className="text-center text-gray-600">
            No skills available. Waiting for game action...
          </p>
        )}
      </div>
    </div>
  );
}
