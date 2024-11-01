import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";

interface Player {
    uid: string,
    stats: {
        [key: string]: number,
    },
    meta: {
        [key: string]: any,
    },
    entities: {
        [key: string]: any,
    },
    collections: {
        [key: string]: any,
    },
    display_name: string,
    description: string,
}

interface GameUIData {
    entities: {
        player: Player
    }
    stats: {
        [key: string]: any,
    }
    meta: {
        [key: string]: any,
    }
    collections: {
        [key: string]: any,
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const getButtonIcon = (slug: string) => {
        switch (slug) {
            case 'play':
                return <Play className="mr-2 h-4 w-4" />;
            case 'quit':
                return <X className="mr-2 h-4 w-4" />;
            default:
                return null;
        }
    };

    return (
        <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8">
            <h1 className="text-4xl md:text-6xl font-bold mt-16">
                {props.data.meta.game_title || "Game Title"}
            </h1>
            
            <div className="flex flex-col items-center space-y-4 mb-16">
                {availableButtonSlugs.map((slug) => (
                    <Button
                        key={slug}
                        uid={`main-menu-${slug}-button`}
                        onClick={() => emitButtonClick(slug)}
                        className="w-48 capitalize"
                    >
                        {getButtonIcon(slug)}
                        {slug}
                    </Button>
                ))}
            </div>
        </div>
    );
}
