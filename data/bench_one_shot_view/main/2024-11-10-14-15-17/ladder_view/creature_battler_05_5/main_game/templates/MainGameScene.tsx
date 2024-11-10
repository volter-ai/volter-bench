import { useCurrentButtons } from "@/lib/useChoices"
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities?.active_creature
  const opponentCreature = props.data.entities.opponent?.entities?.active_creature

  const getCreatureImageUrl = (creature: Creature, isFront: boolean) => 
    `/assets/creatures/${creature.meta.prototype_id}/${isFront ? 'front' : 'back'}.png`

  return (
    <div 
      uid="main-game-container"
      className="h-screen w-full aspect-video flex flex-col bg-gradient-to-b from-blue-100 to-blue-200"
    >
      {/* Battlefield Area (upper 2/3) */}
      <div uid="battlefield-container" className="flex-grow grid grid-cols-2 p-4 gap-4">
        {/* Opponent Side */}
        <div uid="opponent-status-container" className="flex flex-col items-end justify-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={getCreatureImageUrl(opponentCreature, true)}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              className="transform -scale-x-100"
            />
          )}
        </div>
        
        <div uid="opponent-creature-container" className="flex flex-col items-start justify-end">
          {opponentCreature && (
            <div uid={`${opponentCreature.uid}-sprite-container`} className="relative w-48 h-48">
              <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
              <img 
                src={getCreatureImageUrl(opponentCreature, true)}
                alt={opponentCreature.display_name}
                className="w-full h-full object-contain"
              />
            </div>
          )}
        </div>

        {/* Player Side */}
        <div uid="player-creature-container" className="flex flex-col items-end justify-end">
          {playerCreature && (
            <div uid={`${playerCreature.uid}-sprite-container`} className="relative w-48 h-48">
              <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
              <img 
                src={getCreatureImageUrl(playerCreature, false)}
                alt={playerCreature.display_name}
                className="w-full h-full object-contain"
              />
            </div>
          )}
        </div>

        <div uid="player-status-container" className="flex flex-col items-start justify-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={getCreatureImageUrl(playerCreature, false)}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div uid="ui-container" className="h-1/3 bg-white/90 p-4 rounded-t-xl shadow-lg">
        <div uid="button-container" className="flex flex-wrap gap-2">
          {/* Attack Buttons */}
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                accuracy: 100, // Default if not provided
              }}
              variant="default"
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}

          {/* Back Button */}
          {availableButtonSlugs.includes('back') && (
            <Button 
              uid="back-button"
              variant="secondary"
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}

          {/* Swap Button */}
          {availableButtonSlugs.includes('swap') && (
            <Button
              uid="swap-button"
              variant="secondary"
              onClick={() => emitButtonClick('swap')}
            >
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
