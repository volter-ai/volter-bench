import { useCurrentButtons } from "@/lib/useChoices";
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
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
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
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="h-screen w-screen flex items-center justify-center">Loading...</div>;
  }

  const visibleSkills = playerCreature.collections.skills.filter(skill => 
    !availableButtonSlugs || availableButtonSlugs.length === 0 || availableButtonSlugs.includes(skill.uid)
  );

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 bg-slate-200 p-4 gap-4">
        {/* Opponent Status - Top Left */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/assets/creatures/${opponentCreature.meta.prototype_id}.png`}
          />
        </div>

        {/* Opponent Creature - Top Right */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img 
              src={`/assets/creatures/${opponentCreature.meta.prototype_id}.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Player Creature - Bottom Left */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img 
              src={`/assets/creatures/${playerCreature.meta.prototype_id}.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Player Status - Bottom Right */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/assets/creatures/${playerCreature.meta.prototype_id}.png`}
          />
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 bg-slate-100 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {visibleSkills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
