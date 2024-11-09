import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

interface BaseEntity {
    __type: string
    stats: Record<string, number>
    meta: Record<string, string>
    entities: Record<string, any>
    collections: Record<string, any[]>
    uid: string
    display_name: string
    description: string
}

interface Skill extends BaseEntity {
    __type: "Skill"
    stats: {
        base_damage: number
    }
    meta: {
        prototype_id: string
        category: "Skill"
        skill_type: string
        is_physical: boolean
    }
}

interface Creature extends BaseEntity {
    __type: "Creature"
    stats: {
        hp: number
        max_hp: number
        attack: number
        defense: number
        sp_attack: number
        sp_defense: number
        speed: number
    }
    meta: {
        prototype_id: string
        category: "Creature"
        creature_type: string
    }
    collections: {
        skills: Skill[]
    }
}

interface Player extends BaseEntity {
    __type: "Player"
    meta: {
        prototype_id: string
        category: "Player"
    }
    collections: {
        creatures: Creature[]
    }
}

interface GameUIData {
    __type: "MainMenuScene"
    stats: Record<string, number>
    meta: Record<string, string>
    entities: {
        player: Player
    }
    collections: Record<string, any[]>
    uid: string
    display_name: string
    description: string
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    return (
        <div className="relative w-full h-full bg-slate-900">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                <div className="w-full flex-1 flex items-center justify-center">
                    <Card className="bg-slate-800/50 p-8">
                        <h1 className="text-6xl font-bold text-white text-center 
                                     tracking-wider uppercase drop-shadow-lg">
                            {props.data?.display_name || "Game Title"}
                        </h1>
                    </Card>
                </div>

                <div className="w-full max-w-md space-y-4">
                    {availableButtonSlugs.includes('play-game') && (
                        <Button
                            variant="default"
                            size="lg"
                            className="w-full"
                            onClick={() => emitButtonClick('play-game')}
                        >
                            <Play className="w-5 h-5 mr-2" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            variant="destructive"
                            size="lg"
                            className="w-full"
                            onClick={() => emitButtonClick('quit')}
                        >
                            <XCircle className="w-5 h-5 mr-2" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </div>
    )
}
