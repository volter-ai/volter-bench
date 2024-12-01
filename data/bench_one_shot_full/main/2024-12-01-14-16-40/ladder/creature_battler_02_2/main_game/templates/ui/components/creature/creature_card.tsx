import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface CreatureCardBaseProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardContentProps extends CreatureCardBaseProps {
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCardBase = React.forwardRef<HTMLDivElement, CreatureCardBaseProps>(
  ({ className, uid, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("rounded-xl border bg-card text-card-foreground shadow", className)}
      {...props}
    />
  )
)

let CreatureCardHeader = React.forwardRef<HTMLDivElement, CreatureCardBaseProps>(
  ({ className, uid, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex flex-col space-y-1.5 p-6", className)}
      {...props}
    />
  )
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, CreatureCardBaseProps>(
  ({ className, uid, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("font-semibold leading-none tracking-tight", className)}
      {...props}
    />
  )
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, CreatureCardBaseProps>(
  ({ className, uid, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardContentProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <CreatureCardBase ref={ref} uid={`${uid}-base`} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain mb-4"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{`${hp}/${maxHp}`}</span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full">
              <div 
                className="h-full bg-green-500 rounded-full transition-all duration-300"
                style={{ width: `${(hp / maxHp) * 100}%` }}
              />
            </div>
          </div>
        </CreatureCardContent>
      </CreatureCardBase>
    )
  }
)

CreatureCardBase.displayName = "CreatureCardBase"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardTitle.displayName = "CreatureCardTitle"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCard.displayName = "CreatureCard"

CreatureCardBase = withClickable(CreatureCardBase)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardTitle = withClickable(CreatureCardTitle)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
