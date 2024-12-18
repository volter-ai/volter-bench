import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  imageUrl: string
  isPlayer?: boolean
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, imageUrl, isPlayer, ...props }, ref) => {
    return (
      <Card
        ref={ref}
        className={cn("w-[300px]", className)}
        uid={`${uid}-card`}
        {...props}
      >
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`} className="text-center">{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col items-center gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-48 h-48 object-cover rounded-lg"
            />
            <div className="text-xl font-bold">
              HP: {hp}
            </div>
            {isPlayer && (
              <div className="text-sm text-muted-foreground">
                Your Creature
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
