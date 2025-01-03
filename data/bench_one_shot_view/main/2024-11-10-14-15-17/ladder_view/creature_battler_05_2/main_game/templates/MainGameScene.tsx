import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    prototype_id: string
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
  }
}

// Type guards
const isSkill = (item: any): item is Skill => item?.__type === "Skill"
const isCreature = (item: any): item is Creature => item?.__type === "Creature"
const isPlayer = (item: any): item is Player => item?.__type === "Player"

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.opponent?.entities.active_creature

  // Helper to get creature image URL
  const getCreatureImageUrl = (creature: Creature, view: 'front' | 'back') => 
    `/assets/creatures/${creature.meta.prototype_id}/${view}.png`

  return (
    <div className="w-full h-full aspect-video relative bg-slate-900">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex items-start justify-start">
          {opponentCreature && isCreature(opponentCreature) && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={getCreatureImageUrl(opponentCreature, 'front')}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center relative">
          {opponentCreature && isCreature(opponentCreature) && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <img 
                src={getCreatureImageUrl(opponentCreature, 'front')}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            </div>
          )}
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center relative">
          {playerCreature && isCreature(playerCreature) && (
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <img 
                src={getCreatureImageUrl(playerCreature, 'back')}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            </div>
          )}
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-end">
          {playerCreature && isCreature(playerCreature) && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={getCreatureImageUrl(playerCreature, 'back')}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-800/50 p-4">
        <div className="flex flex-wrap gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && 
           playerCreature?.collections.skills.map(skill => {
            if (!isSkill(skill)) return null;
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage,
                  accuracy: 100, // Default values if not provided
                  cost: 0
                }}
              >
                <Sword className="mr-2 h-4 w-4" />
                {skill.display_name}
              </SkillButton>
            );
          })}

          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
