import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
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
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
          <div className="row-start-2 col-start-1 flex items-end justify-start">
            <CreatureCard
              uid={playerCreature?.uid ?? ""}
              name={playerCreature?.display_name ?? "Unknown"}
              image="/path/to/player-creature-back.png"
              hp={playerCreature?.stats.hp ?? 0}
              maxHp={playerCreature?.stats.max_hp ?? 1}
              className="transform scale-x-[-1]"
            />
          </div>
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            <div className="text-right">
              <h3 className="text-lg font-bold">{playerCreature?.display_name}</h3>
              <p>HP: {playerCreature?.stats.hp}/{playerCreature?.stats.max_hp}</p>
            </div>
          </div>
          <div className="row-start-1 col-start-2 flex items-start justify-end">
            <CreatureCard
              uid={opponentCreature?.uid ?? ""}
              name={opponentCreature?.display_name ?? "Unknown"}
              image="/path/to/opponent-creature-front.png"
              hp={opponentCreature?.stats.hp ?? 0}
              maxHp={opponentCreature?.stats.max_hp ?? 1}
            />
          </div>
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            <div className="text-left">
              <h3 className="text-lg font-bold">{opponentCreature?.display_name}</h3>
              <p>HP: {opponentCreature?.stats.hp}/{opponentCreature?.stats.max_hp}</p>
            </div>
          </div>
        </div>
        <div className="h-1/3 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
            {playerCreature?.collections.skills.map((skill) => (
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
      </div>
    </div>
  );
}
